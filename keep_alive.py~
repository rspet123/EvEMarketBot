from flask import Flask
from threading import Thread
from replit import db
app = Flask('')
@app.route('/')
def main():
    outs = "Live:\t"
    return outs
def run():
    app.run(host="0.0.0.0", port=8080)
def keep_alive():
    server = Thread(target=run)
    server.start()