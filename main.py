from fastapi import FastAPI
from pydantic import BaseModel
from utils import *
import nllb
import llama
import consts
from fastapi.responses import StreamingResponse

# JSON format of posted payload
class Payload(BaseModel):
    # the text to translate
    text: str 

# initial loading to take place once
def init():
    err = SUCCESS
    xprint(err,"main init starting...")
    err = llama.init(consts.MODEL_PATH)
    if (not err): err = nllb.init(consts.NLLB_NAME)
    xprint(err,f"main init starting...done err:{err}")

# startup code
app = FastAPI()
init()

# main endpoint
@app.post("/summarize")
async def main(payload: Payload):
    trans_text = nllb.translate(payload.text,"eng_Latn")
    output = llama.chat(trans_text)    
    return StreamingResponse(llama.simple_streamer(output))

