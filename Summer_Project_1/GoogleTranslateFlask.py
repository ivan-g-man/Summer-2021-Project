from flask import Flask, redirect, url_for, render_template, request, session
from googletrans import Translator, LANGUAGES 
from collections import defaultdict 
from urllib.parse import quote_plus
import requests

app = Flask(__name__) 
app.secret_key = "hi"
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
    except Exception as e:
        print("Error in parameters. Check for spelling or white spaces") 
        print(e)
        return "Error in parameters. Check for spelling or white spaces"

#post stuff
def post_api1(excerpt, image, content, title, lang):
    lang_value = get_lang_value(lang)
    response = requests.post('https://happyhappier.wixsite.com/website-1/_functions/stuff?exerpt=' + 
                             quote_plus(excerpt) 
                             + "&img=" + 
                             quote_plus(image) 
                             + "&content=" + 
                             quote_plus(content) 
                             + "&title=" + 
                             quote_plus(title) + "&lang=" + lang_value) 
    return response.json()

my_lang_dict = get_lang_dict(LANGUAGES)
#print("Supported languages:")
#for cur_lang in my_lang_dict:
 #   print(cur_lang)
my_lang_list = []
for cur_lang in my_lang_dict:
    my_lang_list.append(cur_lang)


@app.route("/googletranslate", methods = ["POST", "GET", "PUT"])
def translate(): 
    # return render_template("GoogleTranslate.html")
    if request.method == "POST":
        """
        if request.form.get("post"): # press post button
            post_api1(session["my_excerpt"], session["image_link"], request.form["original_translation"], 
            session["my_title"], session["user_orig_lang"])
            return render_template("GoogleTranslate.html", lang_list = my_lang_list)
        elif request.form.get("submit"): # just submit button
        """
        if request.form.get("submit"): #submit button
            user_url = request.form["url"]
            user_orig_lang = request.form["original language"]
            user_final_lang = request.form["final language"]
            params = {'SM_API_KEY': '947A045DFD', 
            'SM_URL': user_url}
            final_translation = get_input_api_translation(params, user_orig_lang, user_final_lang)
            final_translation_keys = list(final_translation.keys())
            final_translation_values = list(final_translation.values()) 
            my_excerpt = request.form["excerpt"] 
            image_link = request.form["image"] 
            # my_content = request.form["content"] 
            my_title = request.form["title"] 
            #my_post_api = post_api1(my_excerpt, image_link, final_translation_values[0], my_title, user_orig_lang)

            session["my_excerpt"] = my_excerpt 
            session["image_link"] = image_link 
            session["final_translation_keys"] = final_translation_keys 
            session["final_translation_values"] = final_translation_values 
            session["my_title"] = my_title 
            session["user_orig_lang"] = user_orig_lang 

            return redirect(url_for("new_page_stuff", url = user_url, 
            orig_lang = user_orig_lang, final_lang = user_final_lang, lang_list = my_lang_list, 
            orig_key = final_translation_keys[0], final_key = final_translation_keys[1], 
            original_translation = final_translation_values[0], 
            final_translation = final_translation_values[1], 
            excerpt = my_excerpt, image = image_link, title = my_title))  
        """
        return render_template("GoogleTranslate.html", url = user_url, 
            orig_lang = user_orig_lang, final_lang = user_final_lang, lang_list = my_lang_list, 
            orig_key = final_translation_keys[0], final_key = final_translation_keys[1], 
            original_translation = final_translation_values[0], 
            final_translation = final_translation_values[1], 
            excerpt = my_excerpt, image = image_link, title = my_title) 
        """
    else:
        return render_template("GoogleTranslate.html", lang_list = my_lang_list)


@app.route("/googletranslatenewpage", methods = ["POST", "GET"])
def new_page_stuff():
    if request.method == "POST": 
        # my_post = request.form["post"]
        if request.form.get("post"): #post button
            post_api1(session["my_excerpt"], session["image_link"], request.form["original_translation"], 
            session["my_title"], session["user_orig_lang"])
            return redirect(url_for("translate"))
    else:
        return render_template("NewGoogleTranslate.html", url = request.args["url"],  
        orig_lang = request.args["orig_lang"], final_lang = request.args["final_lang"], 
        lang_list = request.args["lang_list"], 
        orig_key = request.args["orig_key"], final_key = request.args["final_key"], 
        original_translation = request.args["original_translation"], 
        final_translation = request.args["final_translation"], 
        excerpt = request.args["excerpt"], image = request.args["image"], 
        title = request.args["title"])


if __name__ == "__main__":
    app.run(debug = True) 
