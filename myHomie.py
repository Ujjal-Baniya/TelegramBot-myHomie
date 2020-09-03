import json
import pyjokes
import requests
import urllib.request

Token = "Enter your bot TOKEN"
Teleurl = "https://api.telegram.org/bot{}".format(Token)

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
    elif "ATT" in msg.upper():
        url = "https://docs.google.com/forms/d/e/1FAIpQLSe_kp3CsZW2I1Q1f5TKMNrrWUkqlnzXTjKw34GkucPiOs1JiQ/formResponse"
        x = updateform('userID,'password',url)
        reply = "response{}".format(x)
    else:
        reply = "I am not intelligent like humans if you want to add feature contact owner https://www.facebook.com/lawju.baniya"
    return reply

def send_message(msg, chat_id, url):
    url = url + "/sendMessage?chat_id={}&text={}".format(chat_id, msg)
    if msg is not None:
        r = requests.get(url)

def updateform(user, passwd,url):
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
    data = {"entry.331168482":"UJJAL BANIYA","entry.1056217443":"18B91A05Q3","entry.2048294415":"Ujjalbaniya@gmail.com"}
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