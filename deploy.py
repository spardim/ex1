import importlib
import os
import subprocess
import sys
import nllb
import llama
from utils import *
import consts

# setup llama.cpp.
# hash: optional commit hash to use. may be None.
# returns: zero on success, non-zero on failures.
def setup_llama(hash):
    
    err = SUCCESS

    if (not os.path.exists(consts.LLAMA_DIR)):
        err = bash("installing llama",None,"git","clone","https://github.com/ggerganov/llama.cpp.git",consts.LLAMA_DIR)
        if ((not err) and hash!=None): 
            err = bash("using specific commit",consts.LLAMA_DIR,"git","checkout",hash)
    else:
        xprint(0,f"llama already exists in {consts.LLAMA_DIR}, no need to clone again")

    if (not err): 
        if (not os.path.exists(consts.LLAMA_DIR + "/llama-cli")):
            err = bash("building llama",consts.LLAMA_DIR,"make") 
    if (not err): 
        err = llama.cli("the weather today is",consts.MODEL_PATH,10)
        if (not err):
            xprint(err,f"llama.cpp verification done. err?:{err}")


    return err

# setup FB nllb
# returns: zero on success, non-zero on failures.
def setup_nllb():

    err = SUCCESS

    module_trans  = bash("checking dependencies 1",None,consts.PIP,"show","transformers",silent=1)
    module_tensor = bash("checking dependencies 2",None,consts.PIP,"show","tensorflow",silent=1)
    module_pytorch = bash("checking dependencies 3",None,consts.PIP,"show","torch",silent=1)

    if (not err and module_trans):
        err = bash("installing transformers",None,consts.PIP,"install","transformers")
    
    if (not err and module_tensor): 
        err = bash("installing tensorflow",None,consts.PIP,"install","tensorflow")
            
    if (not err and module_pytorch):
        err = bash("installing PyTorch",None,consts.PIP,"install","torch","torchvision","torchaudio")

    # need to refresh the installed packages.
    # this still does not work, so you need to re-run deploy.py in case of a missing dependency
    # importlib.util.find_spec("torch", package=None)

    if (not err): 
        xprint(err,f"verifying fb...")
        nllb.init(consts.NLLB_NAME)
        err = int(not nllb.validate("hello world","fra_Latn","Bonjour le monde"))
        xprint(err,f"verifying fb done. err?:{err}")

    return err

# main entry point.
# will try to setup and verify llama.cpp from source code and setup and verify the FB nllb package.
def main():
    
    err = SUCCESS

    # install and verify llama (using specific commit hash that worked for me)
    err = setup_llama("be0cfb41752551a4680ee7dfd29f2a05b50db442")
    
    #  install and verify nllb
    if (not err): err = setup_nllb()
    
    return err


if __name__ == "__main__":
    main()



