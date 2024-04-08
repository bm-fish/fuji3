# Toolkit for processing AIMD result from VASP
## Usage:
Only `energy` sub-function is available now.

    mdkit energy -i ./OUTCAR
    # Output MD run energy statistics
    # outcar.csv will be generated containing statistics of system energy, temperature and nose-hoover thermostat
    mdkit energy -i ./OUTCAR -p
    # Plot the energy statistics in a png file.
    # aimd_energy.png
