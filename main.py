import os
import discord
import csv
from replit import db
import requests
import random
import json
import keep_alive
import time
tk1 = os.environ['TOKEN']
itemdict = {}
fuzzurl1 = "https://market.fuzzwork.co.uk/aggregates/?region="
fuzzurl2 = "&types="
systems = {}
systems["jita"] = "30000142"
systems["perimeter"] = "30000142"
systems["amarr"] = "60008494"
systems["dodixie"] = "60011866"
systems["hek"]= "60005686"
systems["rens"] = "60004588"
url = "https://goonmetrics.apps.goonswarm.org/api/price_data/?station_id=1030049082711&type_id="
moonwalk = ["https://www.youtube.com/watch?v=zvJskQuvypw","https://cdn.discordapp.com/attachments/768592802417999874/841529517696352306/The_escape.mp4","https://youtu.be/-UTAEk22w2A"]
iconurl = "https://images.evetech.net/types/"


def format_num(number):
    out = number
    post = ""
    if number > 1000:
        post = "K"
        out = number / 1000
    if number > 1000000:
        post = "M"
        out = number / 1000000
    if number > 1000000000:
        post = "B"
        out = number / 1000000000
    return (str(round(out, 2)) + post)

def comma_num(number):
    number = round(number,0)
    out = "{:,}".format(number)
    return out


with open('invTypes.csv', newline='') as file1:
    reader = csv.reader(file1)
    for item in reader:
        itemdict[item[2].lower()] = item[0]
client = discord.Client()
print("Starting...")


@client.event
async def on_ready():
    print("GoonBot Running as {0.user}".format(client))
    g = client.guilds
    print("In servers: ")
    for gld in g:
      print(gld)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    item = {}
    if message.content.startswith('!1dq'):
        try:
            start_time = time.time()
            itemname = message.content.split('!1dq ')[1].lower()
            response = requests.get(url + itemdict[itemname])
            cont = str(response.content)
            minsell = float((cont.split("<min>"))[1].split("</min>")[0])
            maxbuy = float((cont.split("<max>"))[1].split("</max>")[0])
            move = float((cont.split("<weekly_movement>")
                          )[1].split("</weekly_movement>")[0])
            print(str(message.author) + " wants " + itemname)
            if str(message.author) in db:
                db[str(message.author)] = db[str(message.author)] + 1
                print(str(message.author) + " has pricechecked " + str(db[str(message.author)]) + " times")
            else:
                db[str(message.author)] = 1
            if(move ==-1):
              await message.channel.send(itemname + " is not currently on the 1DQ1-A market")
              return
            sell1 ="Minimum: " + comma_num(minsell)
            buy1 ="Max: " + comma_num(maxbuy)        
            embed=discord.Embed(title=itemname, description="1DQ1-A", color=0x00fe15)
            embed.set_thumbnail(url=iconurl + itemdict[itemname] + "/icon")
            embed.add_field(name="Sell", value=sell1 + "ƶ", inline=True)
            embed.add_field(name="Buy", value=buy1 + "ƶ", inline=True)
            embed.add_field(name="Weekly Movement", value=comma_num(move), inline=False)
            embed.set_footer(text="Spencer Anders' GoonBot\n" + str(round(time.time() - start_time,3) * 1000)+"ms")
            await message.channel.send(embed=embed)
            
        except Exception:
            await message.channel.send("Try That Again " + message.author.name)
            print(message.author.name + " fucked up")
    if message.content.startswith('!moonwalk'):
      randint = random.randrange(0,len(moonwalk))
      print("Moonwalk #" + str(randint) + " playing")
      await message.channel.send(moonwalk[randint])
    if message.content.startswith("!jita"):
      start_time = time.time()
      if message.author.name == "HamStinkie" or message.author.name == "KATTE":
        await message.channel.send("if you have to ask you can't afford it")
        return
      try:
        itemname = message.content.split('!jita ')[1].lower()
        jitareq = requests.get(fuzzurl1 +systems["jita"] +fuzzurl2+itemdict[itemname])
        iteminf = json.loads(jitareq.text)
        
        buy = iteminf[itemdict[itemname]]["buy"]
        sell = iteminf[itemdict[itemname]]["sell"]
        print("Buy")
        print(buy)
        print("Sell")
        print(sell)
        sell1 = "Minimum: " + comma_num(float(sell["min"]))+ "ƶ\nMedian: " + comma_num(float(sell["median"]))+ "ƶ\nVolume: "+ comma_num(float(sell["volume"])) + "\nOrders: " + comma_num(float(sell["orderCount"]))
        buy1 = "Maximum: " + comma_num(float(buy["max"]))+ "ƶ\nMedian: " + comma_num(float(buy["median"]))+ "ƶ\nVolume: "+ comma_num(float(buy["volume"])) + "\nOrders: " + comma_num(float(buy["orderCount"])) 
        embed=discord.Embed(title=itemname, description="Jita", color=0x00fe15)
        embed.set_thumbnail(url=iconurl + itemdict[itemname] + "/icon")
        embed.add_field(name="Sell", value=sell1, inline=True)
        embed.add_field(name="Buy", value=buy1, inline=True)
        embed.set_footer(text="Spencer Anders' GoonBot\n" + str(round(time.time() - start_time,3) * 1000)+"ms")
        await message.channel.send(embed=embed)
      except Exception:
        await message.channel.send("Try That Again " + message.author.name)
        print(message.author.name + " fucked up")
    if message.content.startswith("!amarr"):
      try:
        start_time = time.time()
        itemname = message.content.split('!amarr ')[1].lower()
        amarrreq = requests.get(fuzzurl1 +systems["amarr"] +fuzzurl2+itemdict[itemname])
        iteminf = json.loads(amarrreq.text)
        
        buy = iteminf[itemdict[itemname]]["buy"]
        sell = iteminf[itemdict[itemname]]["sell"]
        sell1 = "Minimum: " + comma_num(float(sell["min"]))+ "ƶ\nMedian: " + comma_num(float(sell["median"]))+ "ƶ\nVolume: "+ comma_num(float(sell["volume"])) + "\nOrders: " + comma_num(float(sell["orderCount"]))
        buy1 = "Maximum: " + comma_num(float(buy["max"]))+ "ƶ\nMedian: " + comma_num(float(buy["median"]))+ "ƶ\nVolume: "+ comma_num(float(buy["volume"])) + "\nOrders: " + comma_num(float(buy["orderCount"])) 
        embed=discord.Embed(title=itemname, description="Amarr", color=0x00fe15)
        embed.set_thumbnail(url=iconurl + itemdict[itemname] + "/icon")
        embed.add_field(name="Sell", value=sell1, inline=True)
        embed.add_field(name="Buy", value=buy1, inline=True)
        embed.set_footer(text="Spencer Anders' GoonBot\n" + str(round(time.time() - start_time,3) * 1000)+"ms")
        await message.channel.send(embed=embed)
      except Exception:
        await message.channel.send("Try That Again " + message.author.name)
        print(message.author.name + " fucked up")
    if message.content.startswith("!margin"):
      try:
        start_time = time.time()
        color1 = 0x00fe15
        #0x00fe15 Green
        #0xFF0000 Red
        itemname = message.content.split('!margin ')[1].lower()
        amarrreq = requests.get(fuzzurl1 +systems["jita"] +fuzzurl2+itemdict[itemname])
        iteminf = json.loads(amarrreq.text)
        response = requests.get(url + itemdict[itemname])
        cont = str(response.content)
        minsell = float((cont.split("<min>"))[1].split("</min>")[0])
        maxbuy = float((cont.split("<max>"))[1].split("</max>")[0])
        move = float((cont.split("<weekly_movement>"))[1].split("</weekly_movement>")[0])
        buy = iteminf[itemdict[itemname]]["buy"]
        sell = iteminf[itemdict[itemname]]["sell"]
        jita1 = "Min Sell: " + comma_num(float(sell["min"])) +"\nMax Buy: "+comma_num(float(buy["max"])) + "\nVolume: " + comma_num(float(sell["volume"]))
        delve = "Min Sell: " + comma_num(minsell) + "\nMax Buy: " + comma_num(maxbuy)+ "\nVolume: " + comma_num(move)
        nums1 = (minsell- float(sell["min"]))/ minsell
        if nums1 < 0:
          print(nums1)
          color1 = 0xFF0000
        else:
          print(nums1)
          color1 = 0x00fe15
        margins = str(round(((minsell- float(sell["min"]))/ minsell),3)*100)+"%"
        embed=discord.Embed(title=itemname, description="Jita -> 1DQ1-A", color=color1)
        embed.set_thumbnail(url=iconurl + itemdict[itemname] + "/icon")
        embed.add_field(name="1DQ1-A", value=delve, inline=True)
        embed.add_field(name="Jita", value=jita1, inline=True)
        embed.add_field(name="Sell - Sell Margin", value=margins, inline=False)
        embed.set_footer(text="Spencer Anders' GoonBot\n" + str(round(time.time() - start_time,3) * 1000)+"ms")
        await message.channel.send(embed=embed)
      except Exception:
        await message.channel.send("Try That Again " + message.author.name)
        print(message.author.name + " fucked up")
    if message.content.startswith('!kennyg'):
      print('KENNYG')
      await message.channel.send("https://youtu.be/cSg4QeoXS2A")
    if message.content.startswith('!goatse'):
      print('GOATSE')
      await message.channel.send("-ϵ⭕϶-")
    if message.content.startswith('!commands'):
      await message.channel.send("!jita <item>\n!perimeter <item>\n!amarr <item>\n!hek <item>\n!rens <item>\n!dodixie <item>\n!1dq <item>\n!margin <item>\n!compare <buy location> <sell location> <item>")
      await message.channel.send("for example, if i wanted a price check on Caldari Navy Mjolnir Light Missile in Jita, I would say\n!jita Caldari Navy Mjolnir Light Missile")
    if message.content.startswith('!help'):
      print(message.author.name + "wants help lol")
      await message.channel.send("No, lol")
      await message.channel.send("figure it out")
    if message.content.startswith('!porn'):
      print('THETA')
      await message.channel.send("https://goonfleet.com/index.php/topic/140326-squad-theta-squad-no-longer-run-by-angus/")
      await message.channel.send(":skink:")
    if message.content.startswith("!perimeter"):
      try:
        start_time = time.time()
        itemname = message.content.split('!perimeter ')[1].lower()
        perimeterreq = requests.get(fuzzurl1 +systems["perimeter"] +fuzzurl2+itemdict[itemname])
        iteminf = json.loads(perimeterreq.text)
        
        buy = iteminf[itemdict[itemname]]["buy"]
        sell = iteminf[itemdict[itemname]]["sell"]
        sell1 = "Minimum: " + comma_num(float(sell["min"]))+ "ƶ\nMedian: " + comma_num(float(sell["median"]))+ "ƶ\nVolume: "+ comma_num(float(sell["volume"])) + "\nOrders: " + comma_num(float(sell["orderCount"]))
        buy1 = "Maximum: " + comma_num(float(buy["max"]))+ "ƶ\nMedian: " + comma_num(float(buy["median"]))+ "ƶ\nVolume: "+ comma_num(float(buy["volume"])) + "\nOrders: " + comma_num(float(buy["orderCount"])) 
        embed=discord.Embed(title=itemname, description="Perimeter", color=0x00fe15)
        embed.set_thumbnail(url=iconurl + itemdict[itemname] + "/icon")
        embed.add_field(name="Sell", value=sell1, inline=True)
        embed.add_field(name="Buy", value=buy1, inline=True)
        embed.set_footer(text="Spencer Anders' GoonBot\n" + str(round(time.time() - start_time,3) * 1000)+"ms")
        await message.channel.send(embed=embed)
      except Exception:
        await message.channel.send("Try That Again " + message.author.name)
        print(message.author.name + " fucked up")
    if message.content.startswith("!compare "):
      try:
        start_time = time.time()
        color1 = 0x00fe15
        #0x00fe15 Green
        #0xFF0000 Red
        stf1 =  message.content.split(' ',3)
        print(stf1)
        itemname = stf1[3].lower()
        loc1 = stf1[1].lower()
        loc2 = stf1[2].lower()
        print(loc1 + "->" + loc2 + " for "+ itemname)
        json1 = requests.get(fuzzurl1 +systems[loc1] +fuzzurl2+itemdict[itemname])
        json2 = requests.get(fuzzurl1 +systems[loc2] +fuzzurl2+itemdict[itemname])
        print("Got JSON payloads")
        item1 = json.loads(json1.text)
        item2 = json.loads(json2.text)
        print("Loaded JSON")
        buy1 = item1[itemdict[itemname]]["buy"]
        sell1 = item1[itemdict[itemname]]["sell"]
        buy2 = item2[itemdict[itemname]]["buy"]
        sell2 = item2[itemdict[itemname]]["sell"]
        stats1 = "Min Sell: " + comma_num(float(sell1["min"])) +"\nMax Buy: "+comma_num(float(buy1["max"])) + "\nVolume: " + comma_num(float(sell1["volume"]))
        print("Stats 1, Done")
        stats2 = "Min Sell: " + comma_num(float(sell2["min"])) +"\nMax Buy: "+comma_num(float(buy2["max"])) + "\nVolume: " + comma_num(float(sell2["volume"]))
        print("Stats 2, Done")
        nums1 = (float(sell2["min"])- float(sell1["min"]))/ float(sell2["min"])
        print("Margin 1, Done")
        if nums1 < 0:
          print(nums1)
          color1 = 0xFF0000
        else:
          print(nums1)
          color1 = 0x00fe15
        margins = str(round(nums1,3)*100) + "%"
        print("Margin 2, Done")
        embed=discord.Embed(title=itemname.capitalize(), description=loc1.capitalize()+ " -> "+loc2.capitalize(), color=color1)
        embed.set_thumbnail(url=iconurl + itemdict[itemname] + "/icon")
        embed.add_field(name=loc1.capitalize(), value=stats1, inline=True)
        embed.add_field(name=loc2.capitalize(), value=stats2, inline=True)
        embed.add_field(name="Sell - Sell Margin", value=margins, inline=False)
        embed.set_footer(text="Spencer Anders' GoonBot\n" + str(round(time.time() - start_time,3) * 1000)+"ms")
        await message.channel.send(embed=embed)
      except Exception:
        await message.channel.send("Try That Again " + message.author.name)
        print(message.author.name + " fucked up")
keep_alive.keep_alive()
client.run(tk1)

