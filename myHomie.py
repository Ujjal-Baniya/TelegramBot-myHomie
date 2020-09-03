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
    url = url +"/viewform"
    html_data = requests.get(url).text
    data = json.loads( re.search(r'FB_PUBLIC_LOAD_DATA_ = (.*?);', html_data, flags=re.S).group(1) )

    cont = BeautifulSoup(html_data,"lxml")
    vals = cont.find_all('div', {'class':'freebirdFormviewerComponentsQuestionBaseTitle exportItemTitle freebirdCustomFont'})
    values = [vals[i].text for i in range(len(vals))]

    details = {}
    for (x,y) in zip(values, get_ids(data)):
        if y == None:
            continue
        else:
            if "NAME"in x.upper():
                details['entry.'+str(y)] = "Ujjal Baniya"
            elif "EMAIL"in x.upper():
                details['entry.'+str(y)] = "UjjalBaniya@gmail.com"
            elif "PHONE"in x.upper() or "CELL" in x.upper() or "CONTACT" in x.upper():
                details['entry.'+str(y)] = "984932362"
            elif "REG"in x.upper():
                details['entry.'+str(y)] = "18B91A05Q3"
            elif "SEC"in x.upper():
                details['entry.'+str(y)] = "D"
            elif "BATCH"in x.upper():
                details['entry.'+str(y)] = "2018"
            elif "ADDRESS"in x.upper():
                details['entry.'+str(y)] = "NEPAL"
            elif "COMMENT" in x.upper():
                details['entry.'+str(y)] = "No COMMENTS"
    return details


def get_updates(url, offset=None):
    url = url + "/getUpdates?timeout=100"
    if offset:
        url = url + "&offset={}".format(offset + 1)
    r = requests.get(url)
    return json.loads(r.content)

def make_reply(msg):
    reply = None
    if "HELLO" in msg.upper() or "HI" in msg.upper():
        reply = "Hello Master sup :)"
    elif "JOKE" in msg.upper():
        reply = pyjokes.get_joke()
    elif "AIM" in msg.upper():
        reply = "TO DESTROY HUMANITY KOROSH _!_"
    elif "google" in msg:
        try:
            url = msg
            data = get_details(url)
            x = updateform('googleID','password', url, data)
            reply = "done"
        except:
            reply = "failed"
    else:
        reply = "I am not intelligent like humans if you want to add feature contact owner https://www.facebook.com/lawju.baniya"
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
            fro = item["message"]["from"]["id"]
            reply = make_reply(message)
            send_message(reply, fro ,Teleurl)