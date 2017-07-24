# coding: utf-8
"""
Example application showing the use of the Translate method in the Text Translation API.
"""

from xml.etree import ElementTree
from auth import AzureAuthClient
import requests
import codecs

def translate(finalToken, textToTranslate):
    # Call to Microsoft Translator Service
    headers = {"Authorization ": finalToken}
    toLangCode = "en"
    translateUrl = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&to={}".format(textToTranslate.encode('utf-8'), toLangCode)

    translationData = requests.get(translateUrl, headers = headers)
    # parse xml return values
    translation = ElementTree.fromstring(translationData.text.encode('utf-8'))
    # display translation
    print("The translation is---> ", translation.text)
    return translation.text


if __name__ == "__main__":
    client_secret = open("client_secret.txt").readline().strip()

    #client_secret = 'ENTER_YOUR_CLIENT_SECRET'
    auth_client = AzureAuthClient(client_secret)
    bearer_token = 'Bearer ' + str(auth_client.get_access_token())

    #text = "I like"
    #text = u"ثمة"
    f = "/Users/yoshinarifujinuma/work/json_tweets/iran_2013_earthquake.jsonl_tweets.txt"
    startline = 872 + 1 # Line 872 is finished
    #f_out = codecs.open(f + ".en", "w", "utf-8")
    f_out = codecs.open(f + ".en", "a", "utf-8")
    for i, line in enumerate(codecs.open(f, "r", "utf-8")):
        if i < startline - 1:
            # i = 0, startline = 1 => start!
            # i = 0, startline = 2 - 1
            # i = 1, startline = 2 - 1 => start!
            # i = 2, startline = 2 - 1 => start!
            continue
        #print(line)
        translation = translate(bearer_token, line.strip())
        if translation:
            f_out.write(translation + "\n")
        else:
            f_out.write("'None' returned by the API\n")
        if i % 1000 == 0:
            print("finished %i lines" % i)
