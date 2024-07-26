# # Use a pipeline as a high-level helper
# from transformers import pipeline

# print("starting...")

# pipe = pipeline("translation", model="facebook/nllb-200-distilled-600M")

# pipe("This restaurant is awesone")

# print("done")

# -OR-------------------------------------

# # Load model directly
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

# # translate Hindi to French
# hi_text = "जीवन एक चॉकलेट बॉक्स की तरह है।"
# tokenizer.src_lang = "hi"
# encoded_hi = tokenizer(hi_text, return_tensors="pt")
# generated_tokens = model.generate(**encoded_hi, forced_bos_token_id=tokenizer.get_lang_id("en"))
# tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
# # "La vie est comme une boîte de chocolat."


# ---------------------------------------

from utils import *
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

global g_tokenizer
global g_model

def init(name):

    global g_tokenizer
    global g_model

    err = SUCCESS
    xprint(err,"initializing fb nllb...")
    g_tokenizer = AutoTokenizer.from_pretrained(name)
    g_model = AutoModelForSeq2SeqLM.from_pretrained(name)
    if (g_tokenizer == None or g_model == None): err = -1
    xprint(err,f"initializing fb nllb...done. err:{err}")

    return SUCCESS

# returns True on success, False otherwise
def validate(article,target_lang,expected_result):
    result = translate(article,target_lang)
    return (result.lower() == expected_result.lower())


def translate(article,target_lang):

    print(f"translating \"{article}\" to {target_lang}...")

    inputs = g_tokenizer(article, return_tensors="pt")

    translated_tokens = g_model.generate(**inputs, forced_bos_token_id=g_tokenizer.convert_tokens_to_ids(target_lang), max_length=30)
    result = g_tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

    print(f"translating result is \"{result}\"")
    return result



if __name__ == "__main__":
    init()
    validate("hello world","fra_Latn","Bonjour le monde")
