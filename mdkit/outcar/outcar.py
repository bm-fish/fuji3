import sys
import os

# print(sys.path)
sys.path.insert(0, sys.path[0]+"/../")
import util

class Outcar:

    def __init__(self,outcar_dir:str) -> None:
        self.outcar_dir = outcar_dir
        assert os.path.isfile(self.outcar_dir), f"File {self.outcar_dir} does not exist"
        with open(self.outcar_dir, "r") as f:
            first_line = f.readline()
            assert "vasp" in first_line, f"File {self.outcar_dir} Might not contain \"vasp\" "
        f.close()
        self.keywords = {
           'NELM':                True,
           'NSW':                 True,
           'TEBEG':               True,
           'finished_cutcar':     True,
        }

        self.energy_keywords = {
            "free  energy   TOTEN":     True,   #FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)
            "energy  without entropy":  True,
            "energy(sigma->0)":         True,
            "kin. lattice  EKIN_LAT":    True,
            "nose potential ES":         True,
            "nose kinetic   EPS":        True,
            "total energy   ETOTAL":     True,
            "(temperature":               True
        }
        self.energy = {}
        self.energy_start_sign = "FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)"
        self.energy_lines = 46

    def read_energy_term(self):
        self.energy = util.make_data_dict_from_keyword_dict(self.energy_keywords)
        with open(self.outcar_dir, "r") as f:
            lines = f.readlines()
        count = -1  
        # Only enable reading when count < self.energy_lines (around 46)
        # Only enablle reading after a line as sign : self.energy_start_sign 
        #                      "FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)"
        for line in lines:
            if  self.energy_start_sign in line:
                count = 0
            if count <= self.energy_lines and count >= 0:
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

    def __str__(self) -> str:
        outstr = ""
        self.read_energy_term()
        for x in self.energy.keys():
            outstr = outstr+str(x)+"\t"*2+str(len(self.energy[x]))+" in length\n"
        return outstr


if __name__=="__main__":
    outcar1 = Outcar("test/03_fe_mp150/333_md_T500/OUTCAR")
    # print(outcar1.energy_keywords)
    outcar1.read_energy_term()
    print(outcar1)
    # for x in outcar1.energy.keys():
    #     print(x,"\t",len(outcar1.energy[x]))
    # outcar1.write_energy_to_csv("outcar.csv")
    