import pip
import os
import subprocess
import sys

from enum import Enum

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# anything not zero is considered a failure
SUCCESS = 0

# colorized printing
def xprint(err,args):
    if (err): print(bcolors.FAIL + args + bcolors.ENDC)
    else: print(bcolors.OKCYAN + args + bcolors.ENDC)


# run bash command
def bash(tag,dir,*cmd,silent = 0):
    
    ret = SUCCESS

    try:
        xprint(0,f"{tag}...")

        cwd = os.getcwd()
        xprint(0,f"debug cwd is {cwd}")
        if (dir != None):
            os.chdir(dir)

        rp = subprocess.run(cmd)
        # rrr = os.system(cmd)
        if (rp.returncode != 0):
            ret = rp.returncode
            if (not silent): xprint(1,f"{tag}...done with errors")
        else:
            if (not silent): xprint(0,f"{tag}...done ok.")

        if (dir != None):
            os.chdir(cwd)

    except Exception as e:
        ret = -1
        if (not silent): xprint(1,f"{tag} exception. {e}")

    return ret

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)