

URLs = ['https://towardsdatascience.com/6-steps-to-quickly-train-a-human-action-classifier-with-validation-accuracy-of-over-80-655fcb8781c5',
'https://towardsdatascience.com/building-web-app-for-computer-vision-model-deploying-to-production-in-10-minutes-a-detailed-ec6ac52ec7e4',
'https://www.pyimagesearch.com/2018/10/15/deep-learning-hydroponics-and-medical-marijuana/']

from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
import json


json_path = r'ProxySettings.json'
json_path = json_path.replace('\\', '/')
with open(json_path, "r") as read_file:
    proxySettings = json.load(read_file)

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def getBodyText(url):
    #resp = get(url)
    try:
        resp = get(url, proxies = {'https':proxySettings['https']})
        
    except ConnectionError:
        resp = "URL creating problem ConnectionError: " + url
        return {"url": url, "body": resp, "title": resp}
    
    except:
        resp = "Something else went wrong with URL: " + url
        return {"url": url, "body": resp, "title": resp}
        
        
    html = BeautifulSoup(resp.content, 'html.parser')
    remElems = ['style', 'script', 'noscript', 'img']
    for el in remElems:
        for script in html.find_all(el):
            script.decompose()
    title = html.find("title").get_text()
    x=strip_non_ascii(title)
    body = str(html.find("body")) # body.get_text()
    y=strip_non_ascii(body)
    
    re.findall('<.+?>', y)
    y = re.sub('<.+?>', ' ', y)
    
    y = y.replace('\n', ' ')
    y = y.replace('\r', ' ')
    
    return {"url": url, "body": y, "title": x}


myArr = []
for url in URLs:
    myArr.append(getBodyText(url))

df = pd.DataFrame(myArr)

csv_path = r'URLContent1.csv'
csv_path = csv_path.replace('\\', '/')

df.to_csv(csv_path, index=False, columns=['url', 'title', 'body'])

