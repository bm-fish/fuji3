# import glob
# import json
import os
# import shutil
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print(sys.path)
import mdkit
from mdkit.aimd import outcar

outcar1 = outcar.Outcar("test/03_fe_mp150/333_md_T500/OUTCAR")

# print(outcar1)

