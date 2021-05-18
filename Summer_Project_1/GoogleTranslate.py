#Translate
import requests 
from googletrans import Translator, LANGUAGES 
from collections import defaultdict 

"""
trans = Translator()
t = trans.translate("Hola")
print(f"Source: {t.src}")
print(f"Destination: {t.dest}")
print(f"{t.origin} -> {t.text}")
"""
def get_input_api(my_params):
    response = requests.get('https://api.smmry.com',
            params=my_params)
    return response.json() 

#List supported languages
def get_lang_dict(input_dict):
    my_dict = defaultdict(str)
    for cur_key in input_dict:
        my_dict[input_dict[cur_key]] = cur_key
    return dict(my_dict) 

#get value language in dict
def get_lang_value(lang_name):
    my_lang_dict = get_lang_dict(LANGUAGES)
    return my_lang_dict[lang_name.lower()]

#return dictionary of original summary with translation
def get_input_api_translation(my_params, orig_lang, final_lang):
    try:
        my_response_content = get_input_api(my_params)['sm_api_content']
        orig_lang_value = get_lang_value(orig_lang)
        final_lang_value = get_lang_value(final_lang)
        translator = Translator()
        t = translator.translate(src = orig_lang_value, dest = final_lang_value, text = my_response_content)
        orig_lang_copy = orig_lang.upper()
        final_lang_copy = final_lang.upper()
        my_dict = {orig_lang_copy: t.origin, 
                   final_lang_copy: t.text}
        
        for cur_key in my_dict:
            print(cur_key, ":", my_dict[cur_key])  
        return my_dict
    except:
        print("Error in parameters. Check for spelling or white spaces") 
        return "Error in parameters. Check for spelling or white spaces"

my_lang_dict = get_lang_dict(LANGUAGES)
print("Supported languages:")
for cur_lang in my_lang_dict:
    print(cur_lang)

url_input = input("enter URL:")
orig_lang_input = input("enter original language:") 
final_lang_input = input("enter final language:")
params = {'SM_API_KEY': '947A045DFD', 
'SM_URL': url_input}
get_input_api_translation(params, orig_lang_input, final_lang_input) 