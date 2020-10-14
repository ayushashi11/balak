__author__=["Prabhakar Dev"]
input_text=input
print('importing modules..')
import rivescript as rs
from math import *
#from intent import *
from random import randint
from time import *
from pyowm import *
import json,random,sys
import os
from os import getcwd,system,scandir
#from prompt_toolkit.shortcuts import input_dialog,message_dialog as pop
#from wx import App,GetTextFromUser
#input=lambda x:input_dialog("mech'a",x).run()
#input=GetTextFromUser
#from ui import pop
from wikipedia import page,PageError,DisambiguationError
from googlesearch import search as sch
from requests.exceptions import *
from urllib.error import *
from dotenv import load_dotenv
#from telegram import InlineKeyboardButton, InlineKeyboardMarkup
try:
      #import recog                         #comment this line for text input
      input =recog.predict
except BaseException as e:
      print(e.args)
print('setting up...')
key="2223ec0573fa9465ff0aeff7557ccfc8"
owm=OWM(key)
owm=owm.weather_manager()
sadface="😔 😟 ☹ 🥺 😢 😭 😞 😣 😖 😓 😩 😫".split()
#speak=speech.setup_speech()
system('@echo off')
def degrees(temp):
               t=int(temp)
               return str(round(5/9*(t-32)))
def concat(strings):
               c=''
               for string in strings:
                              c+=str(string)
               return c
def s_print(strings,extras=[]):
               for txt in strings:
                              print(txt)
               return ("\n".join(map(str,strings+extras)))
               #speak(concat(strings).replace('\n','. '))
               #pop(concat(strings+extras).replace("\n","."))
def search3(topic):
               try:
                              return s_print(['Here are links:- '],['\n'.join(sch(topic,stop=5))])
               except (ConnectionError,URLError):
                              return s_print(['Unable to Connect'])
               except RuntimeError:
                              return search(topic)
def search2(topic):
               try:
                              return s_print(['Here are links:- '],['\n'.join(sch(topic,stop=10))])
               except (ConnectionError,URLError):
                              return s_print(['Unable to Connect'])
               except RuntimeError:
                              return search3(topic)
def search(topic):
               try:
                              p=page(topic)
                              return s_print([p.title]+p.content.split('.')[:2])
               except PageError:
                              return search2(topic)
               except DisambiguationError:
                              return search2(topic)
               except ConnectionError:
                              return search2(topic)

x=rs.RiveScript(True,depth=1)
#a=App()
code=open('ai2.rive')
x.stream(code.read())
x.sort_replies()
inp=''
s_print(['Hello, Human!'])
def reply(inp): #, up, cqs):
               inp=inp.replace('don\'t','do not').replace('can\'t','cannot').replace('\'ld',' would').replace('\'ll','will').replace('dont','do not').replace('cant','cannot')
               if 'calculate' in inp.lower():
                              if inp.endswith(".."):
                                             return s_print(['Your answer is:- ',eval(inp[inp.index('e')+1:len(inp)].replace('.',''))])
                              else:
                                             return s_print(['Your answer is:- ',eval(inp[inp.index('e')+1:len(inp)])])
               elif 'flip a coin' in inp.lower():
                              ht=['heads','tails']
                              if 'times' in inp.lower():
                                             heads=34
                                             return s_print(['the results are:\n',h,' heads and ',t,' tails'],['\nComplete results are ']+c)
                              else:
                                             return s_print(['It is a '+ht[randint(0,1)]])
               elif 'what is the weather' in inp.lower():
                              try:
                                             obs=owm.weather_at_place('Ranchi,IN')
                                             ret=json.loads(obs.to_JSON())['Weather']
                                             print(ret)
                                             return s_print(['In my city, the weather conditions will most likely be ',ret['detailed_status'],'\nTemperature will remain around ',ret["temperature"]["temp"],' Kelvin ','Humidity ',ret['humidity'],'%. Winds will blow at ',ret['wind']['speed'],' metres per second at ',ret['wind']['deg'],'\u00b0 from North'])
                              except ConnectionError as e:
                                             print(e.args)
                                             return s_print(['NO CONNECTION.\nI cant check the weather without a connection'])
               elif 'search' in inp.lower() or 'google' in inp.lower():
                              s_print(['getting the results...','click OK to continue'])
                              if 'search' in inp.lower():
                                             if 'for' in inp.lower():
                                                            t=inp[inp.index('r',inp.index('f'))+1:len(inp)]
                                                            return search(t)
                                             else:
                                                            t=inp[inp.index('h')+1:len(inp)]
                                                            return search(t)
                              else:
                                             if 'for ' in inp.lower():
                                                            t=inp[inp.index('r ',inp.index('f'))+1:len(inp)]
                                                            return search(t)
                                             else:
                                                            t=inp[inp.index('e')+1:len(inp)]
                                                            return search(t)
               elif (('who is' in inp.lower()) or ('what is' in inp.lower()) or ('where is' in inp.lower())) and not ('your' in inp.lower() or 'this project' in inp.lower()):
                              s_print(['getting the results...','click OK to continue'])
                              y=inp[inp.index('s')+1:len(inp)]
                              return search2(y)
               elif (('who are' in inp.lower()) or ('what are' in inp.lower()) or ('where are' in inp.lower())) and not ('you' in inp.lower() or 'this project' in inp.lower()):
                              s_print(['getting the results...','click OK to continue'])
                              y=inp[inp.index('e')+1:len(inp)]
                              return search2(y)
               elif inp.strip() in sadface:
                              #up.message.reply_text("😃")
                              return s_print(['Dont be sad','smile','😃'])
               else:
                              out=x.reply('user',inp.lower())
                              if out=='code 404':
                                             #keys=[[InlineKeyboardButton("Yes",callback_data="google_yes"),InlineKeyboardButton("No",callback_data="google_no")]]
                                             #rm=InlineKeyboardMarkup(keys)
                                             #id=up.message.from_user.id
                                             #up.message.reply_text("I was unable to process what you said.\nShould I search the internet?",reply_markup=rm)
                                             #cqs.lock().get()[id]={
                                                   #"google_yes":search3(inp.lower()),
                                                   #"google_no":"ok"
                                             #}
                                             #cqs.unlock()
                                             return search3(inp)
                              else:
                                             return s_print([out])
