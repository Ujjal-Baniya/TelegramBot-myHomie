import re
import json
import requests
from bs4 import BeautifulSoup
import pyjokes
import urllib

Token = "Your BOT token ID"
Teleurl = "https://api.telegram.org/bot{}".format(Token)

def get_ids(d):
    if isinstance(d, dict):
        for k, v in d.items():
            yield from get_ids(v)
    elif isinstance(d, list):
        if len(d)>1 and d[1] is None:
            yield d[0]
        else:
            for v in d:
                yield from get_ids(v)

def get_details(url):
    url = url + '/viewform'
    givenData = {
        'name':'Ujjal Baniya',
        'email':'ujjalbaniya@gmail.com',
        'phone': '9391341962',
        'sec':'D',
        'address':'Nepal',
        'comment': 'No comments',
        'reg': '18B1A05Q3'
    }
    url = url +"/viewform"
    html_data = requests.get(url).text
    data = json.loads( re.search(r'FB_PUBLIC_LOAD_DATA_ = (.*?);', html_data, flags=re.S).group(1) )

    cont = BeautifulSoup(html_data,"lxml")
    vals = cont.find_all('div', {'class':'freebirdFormviewerComponentsQuestionBaseTitle exportItemTitle freebirdCustomFont'})
    values = [vals[i].text.rstrip(' *') for i in range(len(vals))]

    details = {}
    for (x,y) in zip(values, get_ids(data)):
        if type(y)==int:
            for key in givenData.keys():
                if key in x.lower():
                    details['entry.'+str(y)] = givenData[key]
    return details


def get_updates(url, offset=None):
    url = url + "/getUpdates?timeout=100"
    if offset:
        url = url + "&offset={}".format(offset + 1)
    r = requests.get(url)
    return json.loads(r.content)

def make_reply(msg, userID):
    reply = None
    if userID == "put your user Id here":
        if "HELLO" in msg.upper() or "HI" in msg.upper():
            reply = "Hello Master sup :)"
        elif "JOKE" in msg.upper():
            reply = pyjokes.get_joke()
        elif "AIM" in msg.upper():
            reply = "TO DESTROY HUMANITY KOROSH _!_"
        elif "google" in msg:
            try:
                msg = msg.split()[1].strip("/viewfrom")
                url = str(msg)
                data = get_details(url)
                x = updateform('dattebayo101a','hell0123', url, data)
                reply = x
            except:
                reply = "failed"
        else:
            reply = "I am not intelligent like humans if you want to add feature contact owner https://www.facebook.com/lawju.baniya"
    else:
        reply = "You are not authorized contact owner https://www.facebook.com/lawju.baniya"
    return reply

def send_message(msg, chat_id, url):
    url = url + "/sendMessage?chat_id={}&text={}".format(chat_id, msg)
    if msg is not None:
        r = requests.get(url)

def updateform(user, passwd, url, data):
    url = url + "/formResponse"
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(
        realm='New mail feed',
        uri='https://mail.google.com',
        user='%s@gmail.com' % user,
        passwd=passwd
    )
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)
    feed = urllib.request.urlopen(url)
    l = requests.post(url, data)
    return l

update_id = None
while True:
    updates = get_updates(Teleurl, offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            try:
                fro = item["message"]["from"]["id"]
            except:
                fro = item['edited_message']["from"]["id"]
                message = "error"
                update_id +=1
            userID = str(fro)
            reply = make_reply(message, userID)
            send_message(reply, fro ,Teleurl)
