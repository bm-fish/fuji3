import sys
import os
import util
import argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# print(sys.path)
from mdkit.aimd.outcar import energy_run

# print(sys.path)
# sys.path.append("/Users/bm.fish/vaspmd")
# from mdkit.outcar import outcar
def main_parser() -> argparse.ArgumentParser:
    """Returns parser for `mdkit` command.

    Returns
    -------
    argparse.ArgumentParser
        parser for `mdkit` command
    """
    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # print("PWD\t:",current_directory)
    parser = argparse.ArgumentParser(
        prog='mdkit', # 程序名
        description="""To see the options for the
    sub-commands, type "mdkit sub-command -h"."""
    )
    subparsers = parser.add_subparsers()

    # ================== Get/plot AIMD energy ===================================
    parser_mdenergy = subparsers.add_parser(
        "energy", help="Get/plot AIMD energy from OUTCAR file"
    )
    parser_mdenergy.add_argument('-p','--plt',action="store_true", help="Add -p/--plt to generate AIMD energy plot from OUTCAR file")
    parser_mdenergy.add_argument('-i','--outcar_dir', type=str,default="./OUTCAR",help="Input OUTCAR file dir")
    parser_mdenergy.set_defaults(func=energy_run)

    # ================== Get/plot AIMD energy ===================================

    return parser

def main():
    print("I am main")
    parser = main_parser()
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        # argcomplete not present.
        pass
    ## Parse the CMD line input
    args = parser.parse_args()
    try:
        getattr(args, "func")
    except AttributeError:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__=="__main__":
    # outcar1 = outcar.Outcar("test/03_fe_mp150/333_md_T500/OUTCAR")
    # print(outcar1.energy_keywords)
    # outcar1.read_energy_term()
    # print(outcar1)
    # for x in outcar1.energy.keys():
    #     print(x,"\t",len(outcar1.energy[x]))
    # outcar1.write_energy_to_csv("outcar.csv")
    main()

    