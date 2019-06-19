from flask import Flask, request, abort, redirect, send_from_directory
import json
import requests
import string
import os
import random

password = ""
client_id = ""
client_secret = ""
with open("config.json") as f:
    config = json.loads(f.read())
    password = config['password']
    client_id = config['client_id']
    client_secret = config['client_secret']

tokenCache = {}
app = Flask(__name__)


def generate_random():
    result = ""
    for i in range(0, 50):
        result += random.choice(string.ascii_letters)
    return result


@app.route('/', methods=['GET'])
def main():
    return """<a href="/github">Register</a>"""


@app.route('/add', methods=['GET'])
def add():
    return send_from_directory('templates', 'add.html')


@app.route('/register', methods=['POST'])
def register():
    if not request.headers['Authorization'] == password:
        abort(403)
    if not request.json:
        abort(400)
    data = request.json
    if \
            'username' not in data or \
            'password' not in data or \
            'server' not in data or \
            'delete' not in data or \
            'ssl' not in data or \
            'gh_token' not in data or \
            'gh_repo' not in data:
        abort(400)
    token_code = data['gh_token']
    if token_code not in tokenCache:
        abort(404)
    if os.path.isfile('accounts/' + request.json['username'] + ".json"):
        abort(409)
    with open("accounts/" + request.json['username'] + ".json", "w") as f:
        data['gh_token'] = tokenCache[token_code]
        tokenCache[token_code] = None
        f.write(json.dumps(request.json))
        f.close()
    return json.dumps({"message": "Success"})


@app.route('/github', methods=['GET'])
def gh():
    return redirect("https://github.com/login/oauth/authorize?client_id=" + client_id + "&scope=repo&allow_signup=false")


@app.route('/github/auth', methods=['GET'])
def callback():
    if 'code' not in request.args:
        abort(400)
    code = request.args['code']
    response = requests.post("https://github.com/login/oauth/access_token", {"client_id": client_id, "client_secret": client_secret, "code": code}, headers={"Accept": "application/json"})
    token_id = generate_random()
    if 'access_token' not in response.json():
        abort(400)
    tokenCache[token_id] = response.json()['access_token']
    return redirect('/add#' + token_id)


if __name__ == '__main__':
    app.run()
