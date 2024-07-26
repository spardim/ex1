from utils import *
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

global g_tokenizer
global g_model

# call init() before using this package
# name: model name to use
# returns: zero on success, non-zero on failures.
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

# validate translation is correct
# article: text to translate
# target_lang: target language
# expected_result: expected result
# returns: True on success, False otherwise
def validate(article,target_lang,expected_result):
    result = translate(article,target_lang)
    return (result.lower() == expected_result.lower())


# translate givven article to target_lang
# returns: the resulting translation
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
