import os
## Add parrent dir in path
current_dir = os.path.dirname(os.path.realpath(__file__))
__path__.append( 
    os.path.abspath(os.path.join(current_dir, '..'))
)
print("Initialising outcar model")
print(__path__)
print("End initialising")
