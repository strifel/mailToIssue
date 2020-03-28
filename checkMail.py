from imbox import Imbox
import json
from datetime import datetime, timedelta
import os
import requests

print("Running mailToIssue!")

for fileName in os.listdir("accounts/"):
    username = ""
    password = ""
    server = ""
    repo = ""
    token = ""
    ssl = True
    delete_after = 0

    with open("accounts/" + fileName) as f:
        config = json.load(f)
        username = config['username']
        password = config['password']
        server = config['server']
        repo = config['gh_repo']
        token = config['gh_token']
        if 'ssl' in config:
            ssl = config['ssl']
        if 'delete' in config:
            delete_after = int(config['delete'])
            if delete_after < 0:
                delete_after = 0
    print("Config for " + username + " loaded!")

    with Imbox(server,
               username=username,
               password=password,
               ssl=ssl) as inbox:
        print("Connected...", end="")
        inbox_messages = inbox.messages(unread=True)
        print("mails loaded")
        for uid, message in inbox_messages:
            issueReport = ""
            issueReport += "# " + message.subject + "\r\n"
            issueReport += "Reported by: [" + message.sent_from[0]['name'] + "](mailto:" + message.sent_from[0][
                'email'] + ")\r\n"
            for line in message.body['plain']:
                issueReport += line
            inbox.mark_seen(uid)
            response = requests.post('https://api.github.com/repos/' + repo + '/issues', json={
                'title': message.subject,
                'body': issueReport
            }, headers={
                'Authorization': 'token ' + token
            })
            print("Issue " + message.subject + " created!")

        if delete_after > 0:
            date = datetime.now() - timedelta(days=delete_after)
            need_to_deleted = inbox.messages(date__lt=date)
            for uid, message in need_to_deleted:
                inbox.delete(uid)
