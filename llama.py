from typing import Generator
import consts
from utils import *
from llama_cpp import Llama

global g_llm

def init(model):
    
    global g_llm
    err = SUCCESS
    
    xprint(err,"initializing cpp llama...")
    g_llm = Llama(model_path=model)
    if (g_llm == None): err = -1
    xprint(err,f"initializing cpp llama...done. init:{err}")
    
    return err

def cli(text,gguf,n):

    err = SUCCESS
    # err = bash("running llama",LLAMA_DIR,"./llama-cli","--n-gpu-layers","0","-m","../Phi-3-mini-4k-instruct-q4.gguf","-p",text,"-n","40")
    err = bash("running llama",consts.LLAMA_DIR,"./llama-cli","--n-gpu-layers","0","-m",gguf,"-p",text,"-n",str(n))
    return err


def simple_streamer(stream_data) -> Generator:
    
    for chunk in stream_data:
        delta = chunk['choices'][0]['delta']
        if 'role' in delta:
            pass
            # yield delta['role']
        elif 'content' in delta:
            yield delta['content']

def chat(text):

    # output = llm("Q: Name the planets in the solar system? A: ", # Prompt
    #   max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
    #   stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
    #   echo=True # Echo the prompt back in the output
    # ) # Generate a completion, can also call create_completion

    # output: Iterator[CreateCompletionStreamResponse]

    # output = llm.create_completion(trans_text, # Prompt
    #   max_tokens=128, # Generate up to 32 tokens, set to None to generate up to the end of the context window
    #   stream=True,
    #   stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
    #   echo=True # Echo the prompt back in the output
    # ) # Generate a completion, can also call create_completion

    output = g_llm.create_chat_completion(
        messages=[
            { "role": "system", "content": "You are my assistant." },
            { "role": "user", "content": text} ],
        stream=True,
        # max_tokens=100
    )
    return output

