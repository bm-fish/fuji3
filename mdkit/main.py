import sys
import os
import util
# print(sys.path)
sys.path.append("/Users/bm.fish/vaspmd")
from mdkit.outcar import outcar

if __name__=="__main__":
    outcar1 = Outcar("test/03_fe_mp150/333_md_T500/OUTCAR")
    # print(outcar1.energy_keywords)
    outcar1.read_energy_term()
    print(outcar1)
    # for x in outcar1.energy.keys():
    #     print(x,"\t",len(outcar1.energy[x]))
    # outcar1.write_energy_to_csv("outcar.csv")