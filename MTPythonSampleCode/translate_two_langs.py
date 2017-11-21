# coding: utf-8
"""
Example application showing the use of the Translate method in the Text Translation API.
"""

from xml.etree import ElementTree
from auth import AzureAuthClient
import requests
import codecs
import time
import urllib

# TODO: Modify this script to translate into two different languages
target_langs = ["en", "es", "pt"]

#def write_translation(bearer_token, line, form_lang, tolang):
#    f_out = codecs.open(f + "." + tolang, "a", "utf-8")
#    translation = translate(bearer_token, line.strip(), from_lang)
#    f_out.write(translation + "\n")

def translate(finalToken, textToTranslate, fromLangCode, toLangCode):
    # Call to Microsoft Translator Service
    headers = {"Authorization ": finalToken}
    #toLangCode = "en"
    #toLangCode = "pt"
    #translateUrl = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&to={}".format(textToTranslate.encode('utf-8'), toLangCode)
    translateUrl = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&to={}&from={}".format(textToTranslate.encode('utf-8'), toLangCode, fromLangCode)

    translationData = requests.get(translateUrl, headers = headers)
    # parse xml return values
    translation = ElementTree.fromstring(translationData.text.encode('utf-8'))
    # display translation
    print("The translation is---> ", translation.text)
    return translation.text


if __name__ == "__main__":
    #client_secret = open("client_secret.txt").readline().strip()
    client_secret = open("client_secret_michael.txt").readline().strip()
    #client_secret = open("client_secret_2.txt").readline().strip()
    auth_client = AzureAuthClient(client_secret)
    bearer_token = 'Bearer ' + str(auth_client.get_access_token())

    #text = "I like"
    #text = u"ثمة"
    #data_dir = "/Users/yoshinarifujinuma/work/zika-paul/"
    data_dir = "/home/yofu1973/work/zika-paul/data/"
    f = data_dir + "uniformly_sampled_zika_tweets_url_user_hashtags_del.txt"
    f_attr = data_dir + "uniformly_sampled_zika_tweets_url_user_hashtags_del_attributes.txt"

    langs = []# list of langauges of tweets. indice i = tweet i
    for line in codecs.open(f_attr, "r", "utf-8"):
        cols = line.strip().split()
        lang = cols[0]
        langs.append(lang)
    #startline = 1
    startline = 2001 # TODO: be sure to update this
    #startline = 3174 + 1 # Resume at the point that was fdone
    #f_out = codecs.open(f + ".en", "w", "utf-8")
    #f_out = codecs.open(f + ".en", "a", "utf-8")
    #f_out = codecs.open(f + ".pt", "a", "utf-8")
    none_returned = 0
    for i, line in enumerate(codecs.open(f, "r", "utf-8")):
        if i == 10000: break
        from_lang = langs[i]
        to_langs = []
        # translate to two other languages
        for lang in target_langs:
            if not lang == from_lang:
                to_langs.append(lang)
        assert(len(to_langs) == 2)
        
        #time.sleep(1)
        if i < startline - 1:
            # i = 0, startline = 1 => start!
            # i = 0, startline = 2 - 1
            # i = 1, startline = 2 - 1 => start!
            # i = 2, startline = 2 - 1 => start!
            continue
        #print(line)

        f_out = codecs.open(f + "." + from_lang, "a", "utf-8") # org. lang
        f_out.write(line)

        for to_lang in to_langs:
            temp = urllib.quote(line.strip().encode("utf-8"))
            #translation = translate(bearer_token, line.strip(), from_lang, to_lang)
            translation = translate(bearer_token, temp, from_lang, to_lang)
            if translation:
                f_out = codecs.open(f + "." + to_lang, "a", "utf-8")
                f_out.write(translation + "\n")
                none_returned = 0
            else:
                f_out = codecs.open(f + "." + to_lang, "a", "utf-8") # Be sure to open and write at every time
                f_out.write("'None' returned by the API\n")
                none_returned += 1
                if none_returned >= 10: break
        if i % 1000 == 0:
            print("finished %i lines" % i)
            
