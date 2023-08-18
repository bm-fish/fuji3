import sys
import os
import matplotlib.pyplot as plt
SMALL_SIZE = 16
MEDIUM_SIZE = 18
BIGGER_SIZE = 24
plt.rcParams["font.family"] = "Times New Roman"
plt.rc('font', size=18)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
# plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
# plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
# plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
# plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

import numpy as np

# print(sys.path[0])
# sys.path.insert(0, sys.path[0]+"/../")
from mdkit import util

class Outcar:

    def __init__(self,outcar_dir:str) -> None:
        self.outcar_dir = outcar_dir
        util.check_outcar_exist(outcar_dir)

        self.keywords = {
           'NELM':                True,
           'NSW':                 True,
           'TEBEG':               True,
           'finished_cutcar':     True,
        }

        self.energy_keywords = {
            "free  energy   TOTEN":     True,   #0 FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)
            "energy  without entropy":  True,   #1
            "energy(sigma->0)":         True,   #2
            "kinetic energy EKIN":      True,   #3
            "kin. lattice  EKIN_LAT":    True,  #4
            "nose potential ES":         True,  #5
            "nose kinetic   EPS":        True,  #6
            "total energy   ETOTAL":     True,  #7
            "(temperature":               True  #8
        }
        self.energy = {}
        self.__energy_start_sign__ = "FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)"
        self.__energy_lines__ = 46

    def read_energy_term(self):
        self.energy = util.make_data_dict_from_keyword_dict(self.energy_keywords)
        with open(self.outcar_dir, "r") as f:
            lines = f.readlines()
        count = -1  
        # Only enable reading when count < self.energy_lines (around 46)
        # Only enablle reading after a line as sign : self.__energy_start_sign__ 
        #                      "FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)"
        for line in lines:
            if  self.__energy_start_sign__ in line:
                count = 0
            if count <= self.__energy_lines__ and count >= 0:
                count += 1
                for key in self.energy_keywords.keys():
                    if self.energy_keywords[key] is not False:
                        # WHen the value in energy_keywords is not False, read the energy data. Or keep the value as False
                        line_find = util.find_num_after_searchstr(line,key,dtype="float")
                        if line_find is not None:
                            self.energy[key].append(line_find)

    
    def write_energy_to_csv(self,csv_dir):
        if len(self.energy) <= 0:
            raise(RuntimeError,"Run self.read_energy_term() first, to get self.energy")
        util.write_data_dict_to_csv(self.energy,csv_dir)

    def plot_sys_energy(self):
        energy_keywords = tuple(self.energy_keywords.keys())

        # SYS parameters
        T = self.energy[energy_keywords[8]]
        TOTEN = self.energy[energy_keywords[0]]
        E_woTS = self.energy[energy_keywords[1]]
        E0 = self.energy[energy_keywords[2]]
        EKIN = self.energy[energy_keywords[3]]
        EKIN_LAT = self.energy[energy_keywords[4]]
        ETOTAL = self.energy[energy_keywords[7]]
        
        # Nose thermostat
        ES = self.energy[energy_keywords[5]] # Nose potential E
        EPS = self.energy[energy_keywords[6]] # Nose kinetics E

        # Steps
        maxlen = util.get_dict_max_len(self.energy)
        x = np.array(range(maxlen))+1

        # =====================  PLOT ==============================
        # Create a figure and a 1x2 subplot grid =============================
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

        # Plot data on the first subplot
        line1_1, = axs[0].plot(x, T, '-k', label='Temp')
        axs[0].set_title('System Energy')
        axs[0].set_xlabel('Steps')  # X label for the first subplot
        axs[0].set_xlim([0,maxlen])
        axs[0].set_ylabel('Temperature [K]')       # Primary Y label for the first subplot


        # Add secondary y-axis to the first subplot ==========================
        ax1_twin = axs[0].twinx()
        line1_2, = ax1_twin.plot(x, TOTEN, '-g', label='Potential Energy')
        ax1_twin.set_ylabel('Energy [eV]',rotation=-90,labelpad=20)

        # Combine lines and labels from both y-axes for a single legend
        lines_1 = [line1_1, line1_2]
        labels_1 = [l.get_label() for l in lines_1]
        axs[0].legend(lines_1, labels_1, loc='lower right')

        # Plot data on the second subplot =====================================
        line2_1, = axs[1].plot(x, T, '-k', label='Temp')
        axs[1].set_title('Nose thermostat Energy')
        axs[1].set_xlabel('Steps')  # X label for the second subplot
        axs[0].set_xlim([0,maxlen])
        axs[1].set_ylabel('Temperature [K]')       # Primary Y label for the second subplot

        # Add secondary y-axis to the second subplot
        ax2_twin = axs[1].twinx()
        line2_2,= ax2_twin.plot(x, ES, '-b', label='Nose-potential')
        line2_3,= ax2_twin.plot(x, EPS, '-m', label='Nose-kinetics')
        ax2_twin.set_ylabel('Energy [eV]',rotation=-90,labelpad=20)

        # Combine lines and labels from both y-axes for a single legend =========
        lines_2 = [line2_1, line2_2,line2_3 ]
        labels_2 = [l.get_label() for l in lines_2]
        axs[1].legend(lines_2, labels_2, loc='lower right')

        # Adjust layout to prevent overlap ======================================
        plt.tight_layout()
        # Save the figure to a file
        plt.savefig('aimd_energy.png')

        # Optionally display the plots
        # plt.show()


    ## Function for print
    def __str__(self) -> str:
        outstr = ""
        self.read_energy_term()
        for x in self.energy.keys():
            outstr = outstr+str(x)+"\t"*2+str(len(self.energy[x]))+" in length\n"
        return outstr



def energy_run(args):
    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # print("PWD :",current_directory)
    ## Check Input OUTCAR dir
    outcar_absdir = os.path.abspath(args.outcar_dir)
    print("Checking OUTCAR dir :",outcar_absdir)
    util.check_outcar_exist(outcar_absdir)

    # Print input args
    print("Input args:")
    print("Plot: ", args.plt)
    print("OUTCAR dir: ",args.outcar_dir)
    
    # Runctions
    outcar1 = Outcar(outcar_absdir)
    outcar1.read_energy_term()
    print(outcar1.energy_keywords)
    # outcar1.write_energy_to_csv("outcar.csv")
    # print(list(outcar1.energy_keywords.keys()))
    # print(outcar1.energy["free  energy   TOTEN"])
    if args.plt is True:
        outcar1.plot_sys_energy()

if __name__=="__main__":
    # outcar1 = Outcar("test/03_fe_mp150/333_md_T500/OUTCAR")
    # print(outcar1.energy_keywords)
    # outcar1.read_energy_term()
    # print(outcar1)
    # for x in outcar1.energy.keys():
    #     print(x,"\t",len(outcar1.energy[x]))
    # outcar1.write_energy_to_csv("outcar.csv")
    # from 
    pass
    