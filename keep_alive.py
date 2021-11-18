from flask import Flask
from flask import render_template
from flask import Markup
from threading import Thread
from replit import db
import db_inspect
import updaters
app = Flask('')
@app.route('/')
def main():
    outs = ""
    for key1 in db.keys():
      outs = outs + key1
    return render_template("webapp.html")
@app.route('/stats/')
def stats():
    return render_template('stats.html')
@app.route('/users/')
def users():
    return render_template('users.html')
@app.route('/graph/')
def graph():
    updaters.make_user_graph()
    return render_template('graph.html')
@app.route('/items/')
def items():
    updaters.make_item_graph()
    return render_template('item_graph.html')
def run():
    app.run(host="0.0.0.0", port=8080)
def keep_alive():
    server = Thread(target=run)
    server.start()