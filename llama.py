from typing import Generator
import consts
from utils import *
from llama_cpp import Llama

global g_llm

# call init() before using this package
# model: the model name to use
# returns: zero on success, non-zero on failures.
def init(model):
    
    global g_llm
    err = SUCCESS
    
    xprint(err,"initializing cpp llama...")
    g_llm = Llama(model_path=model)
    if (g_llm == None): err = -1
    xprint(err,f"initializing cpp llama...done. init:{err}")
    
    return err


# run llama-cli
# returns: zero on success, non-zero on failures.
# text: the text to prompt with
# gguf: the model path to use
# n: limit result tokens.
def cli(text,gguf,n=0):

    err = SUCCESS
    if (n > 0):
        err = bash("running llama",consts.LLAMA_DIR,"./llama-cli","--n-gpu-layers","0","-m",gguf,"-p",text,"-n",str(n))
    else:
        err = bash("running llama",consts.LLAMA_DIR,"./llama-cli","--n-gpu-layers","0","-m",gguf,"-p",text)
    return err


# returns a generator from stream_data
def simple_streamer(stream_data) -> Generator:
    
    for chunk in stream_data:
        delta = chunk['choices'][0]['delta']
        if 'role' in delta:
            pass
            # yield delta['role']
        elif 'content' in delta:
            yield delta['content']

# execute a chat using the given text
def chat(text):

    output = g_llm.create_chat_completion(
        messages=[
            { "role": "system", "content": "You are my assistant." },
            { "role": "user", "content": text} ],
        stream=True,
        # max_tokens=100
    )
    return output

