import discord
import os
import requests
import json
import random
import time
from discord.ext import tasks
from datetime import datetime
from datetime import timedelta
from pytz import timezone 
import pytz
from os import path
from keep_alive import keep_alive


intents = discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)

#Greetings#
Greetings = ["Hi there!","Hello!","Hola!", "Bonjour!","Aloha!", "Hey you!"]
#Greetings#

Praise_list= ["You are awesome!", "Great job!", "You are the best!", "You rock!", "Nicely done!", "Good going!", "That is the right spirit", "good stuff", "well done"]

Cheating_list = ["You cant cheat me", "Don't Lie", "You are done for the day", "Once a cheater, always a repeater" ]


#teasing#
teasing_list = ["I have a life, other then serving you!", "I am busy, text me later!", "You are so need!", "come on! give me a break"]
kidding=["**Just Kidding!**","**Ha Ha! I'm teasing you!**", "**Bazinga!!**","**Fooled you!**"]
def teasing():
  i = read_File("txtfiles/menction.txt")
  menction = int(i)+1

  if menction>=2:
    menction = 0
    write_File("txtfiles/menction.txt",menction)
    return True
  else:
    write_File("txtfiles/menction.txt",menction)
    return False
#teasing

#inspire#
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
#inspire#

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  # message_channel = client.get_channel(int(os.getenv('ChannelID')))
  

  # if any(word in message.content for word in Greetings):
  #   await message.channel.send('Hello!')
  #   await message_channel.send("https://www.youtube.com/watch?v=ZDd_HMd_E7g")

  if client.user.mentioned_in(message):
    random_greeting = random.choice(Greetings)
    if teasing():
      time.sleep(2)
      random_teasing = random.choice(teasing_list)
      await message.channel.send(random_teasing)
      time.sleep(5)
      random_kid = random.choice(kidding)
      await message.channel.send(random_kid)
    else:
      await message.channel.send(random_greeting)

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('$workoutplan'):
    embed=discord.Embed(title=f"Workout Plan",description=read_File("txtfiles/workoutPlan.txt"),color=discord.Color.green())
    await message.channel.send(embed=embed)
  
  if message.content.startswith("$day1") or message.content.startswith("$day3") or message.content.startswith("$day5"):
    embed=discord.Embed(title=f"Strength training",description=read_File("txtfiles/StrengthTraining.txt"),color=discord.Color.green())
    await message.channel.send(embed=embed)

  if message.content.startswith("$day2"):
    embed=discord.Embed(title=f"High-intensity interval training",description=read_File("txtfiles/HigInv_training.txt"),color=discord.Color.green())
    await message.channel.send(embed=embed)
  
  if message.content.startswith("$day4"):
    embed=discord.Embed(title=f"Steady-State Cardio",description=read_File("txtfiles/SteadyState_Cardio.txt"),color=discord.Color.green())
    await message.channel.send(embed=embed)
  
  restday = ["restday_five.jpg","restday_four.jpg","restday_one.jpg","restday_three.png","restday_two.jpg","Restday.jpg"]

  if message.content.startswith("$day6") or message.content.startswith("$day7"):
    random_img = random.choice(restday)
    rest_img = open('restday_imgs/'+random_img, 'rb')
    picture = discord.File(rest_img)
    await message.channel.send(file=picture)
  
  if message.content.startswith("$done_d"):
    if verify_canupdate(message):
      random_praise = random.choice(Praise_list)
      await message.channel.send(random_praise)
      if workout_day(message):
        workourDay = workout_day(message)
        msg = read_File("Users_data/"+str(message.author.id)+".json")
        data = json.loads(msg)
        data["Day"+workourDay] = "Done"
        data["LMd"] = str(getCurrent_DateTime())
        msg = json.dumps(data,indent = 4)
        write_File("Users_data/"+str(message.author.id)+".json",msg)
    else:
      random_cheating = random.choice(Cheating_list)
      await message.channel.send(random_cheating)
      await message.channel.send("Come back tomorrow")

  if message.content.startswith('$Time'):
    await message.channel.send(getCurrent_DateTime())
    

def workout_day(message):
  if message.content.startswith("$done_d"):
    return message.content[7]
  else:
    return None
  

def verify_canupdate(message):
    utc=pytz.UTC
    return_val = False
    msg = read_File("Users_data/"+str(message.author.id)+".json")
    data = json.loads(msg)
    LastModified_time = data["LMd"]
    LastModified_date = data["LMd"]
    if LastModified_date: 
      LastModified_time = datetime.strptime(LastModified_time, '%d/%m/%Y %H:%M:%S')
      LastModified_time = utc.localize(LastModified_time)
      LastModified_time = LastModified_time + timedelta(hours=10)
      LastModified_time = LastModified_time.time()
      Morning_time = LastModified_time.replace(hour=5, minute=30, second =0)      

      LastModified_date = datetime.strptime(LastModified_date, '%d/%m/%Y %H:%M:%S')
      LastModified_date = utc.localize(LastModified_date)
      LastModified_date = LastModified_date.date()

      cur_DateTime = getCurrent_DateTime()
      cur_DateTime = datetime.strptime(cur_DateTime, '%d/%m/%Y %H:%M:%S')
      cur_DateTime = utc.localize(cur_DateTime)

      if cur_DateTime.time() > Morning_time and cur_DateTime.date() > LastModified_date:
        return_val = True
      else:
        return_val = False
    else:
      return_val = True
    return return_val

def getCurrent_DateTime():
  india = timezone('Asia/Calcutta')
  now = datetime.now(india)
  return  str(now.strftime("%d/%m/%Y %H:%M:%S"))

def create_user(filename,username):
  User_data ={
    "name" : username,
    "ID" : filename,
    "LMd" : "",
    "Day1" : "",
    "Day2" : "",
    "Day3" : "",
    "Day4" : "",
    "Day5" : "",
  }
  json_object = json.dumps(User_data, indent = 4)
  write_File("Users_data/"+str(filename)+".json",json_object)


def getCurrentTime():
    now = datetime.now()
    return str(now.strftime("%d/%m/%Y %H:%M:%S"))

def Calculate_totalTime(startTime):
  time.sleep(10)
  startTime = datetime.strptime(startTime, '%d/%m/%Y %H:%M:%S')
  totalTime = str(datetime.now()-startTime)
  return totalTime

def reset_days(jsonPath):
  msg = read_File(jsonPath)
  data = json.loads(msg)
  data["Day1"] = ""
  data["Day2"] = ""
  data["Day3"] = ""
  data["Day4"] = ""
  data["Day5"] = ""
  msg = json.dumps(data,indent = 4)
  write_File(jsonPath,msg)


def clearFor_week():
  utc=pytz.UTC
  cur_DateTime = getCurrent_DateTime()
  cur_DateTime = datetime.strptime(cur_DateTime, '%d/%m/%Y %H:%M:%S')
  cur_DateTime = utc.localize(cur_DateTime)
  sunday_night = cur_DateTime.replace(hour=20, minute=30, second =0)
  if datetime.today().weekday() == 6 and cur_DateTime.time() > sunday_night.time():
    for guild in client.guilds:
      for member in guild.members:
        jsonPath = "Users_data/"+str(member.id)+".json"
        if path.exists(jsonPath):
          reset_days(jsonPath)

def getVideo_url():
  url = "Howdy!"
  YObj = open("txtfiles/YoutubeVideos.txt","r")
  url_list = YObj.readlines()
  url = url_list[1]
  YObj.close()
  return url

def updateVideo_url():
  YObj = open("txtfiles/YoutubeVideos.txt","r")
  url_list = YObj.readlines()
  url_list[0] = getCurrent_DateTime()
  del url_list[1]
  YObj.close()
  YObj = open("txtfiles/YoutubeVideos.txt","w")
  for i in url_list:
    YObj.write(str(i).strip()+"\n")
  YObj.close()
        
def Youtube_post():
  utc=pytz.UTC
  url = "Howdy!"
  cur_DateTime = getCurrent_DateTime()
  cur_DateTime = datetime.strptime(cur_DateTime, '%d/%m/%Y %H:%M:%S')
  cur_DateTime = utc.localize(cur_DateTime)
  every_mornig = cur_DateTime.replace(hour=8, minute=30, second =0)

  YObj = open("txtfiles/YoutubeVideos.txt","r")
  url_list = YObj.readlines()
  pre_date = str(url_list[0]).strip()
  YObj.close()
  pre_date = datetime.strptime(pre_date, '%d/%m/%Y %H:%M:%S')
  pre_date = utc.localize(pre_date)
  
  if cur_DateTime.time() > every_mornig.time() and cur_DateTime.date() > pre_date.date():
    url = getVideo_url()
    updateVideo_url()
  return str(url).strip()
    

@tasks.loop(hours = 4) # repeat after every 24 hours
async def myLoop():
  clearFor_week()

myLoop.start()

#read txt file#
def read_File(filepath):
  fileObj = open(filepath,"r")
  Msg=fileObj.read()
  fileObj.close()
  return Msg
#read txt file#

#write txt file
def write_File(filepath,msg):
  fileObj = open(filepath,"w")
  fileObj.write(str(msg))
  fileObj.close()
#write txt file

#welcome message#

@client.event
async def on_member_join(member):
  embed=discord.Embed(title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!"+"\n"+read_File("txtfiles/welcome.txt"),color=discord.Color.green())
  embed.set_thumbnail(url=member.avatar_url)
  await member.send(embed=embed)
  create_user(member.id,member.name)

def delete_user(member):
  os.remove("Users_data/"+str(member.id)+".json")

@client.event
async def on_member_remove(member):
  delete_user(member)

#welcome message#
keep_alive()
client.run(os.getenv('TOKEN'))