import pandas as pd
from replit import db
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.express as px

def console_stat_updater():
  for key in db.keys():
    print(key.split("#")[0] + ":" + str(db[key]))

def make_user_graph():
  users = []
  data = []
  for key in db.keys():
    if "#" in key:
      users.append(key)
      data.append(db[key])
  fig = px.bar(x=users, y=data)
  fig.write_html("templates/graph.html")

def make_item_graph():
  items = []
  data = []
  for key in db.prefix("Item: "):
    items.append(key)
    data.append(db[key])
  fig = px.bar(x=items, y=data)
  fig.write_html("templates/item_graph.html")