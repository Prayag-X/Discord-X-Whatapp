from re import search
import discord
import selenium
import os
import pyperclip
import time
import logging
import requests
import json

from discord import channel
from discord.embeds import Embed
from discord.ext import commands
from discord.team import Team
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webbrowser import Chrome
from bs4 import BeautifulSoup

from Bot_Data import *
from Util import *

client=commands.Bot(command_prefix='')


class Whatsapp:
    chrome = None
    wapweb = 'https://web.whatsapp.com/'

    search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
    sender_xpath = '//span[@class="matched-text i0jNr"]'
    parent_xpath = '//span[.//span[@class="matched-text i0jNr"]]'
    input_xpath = '//div[@title="Type a message"]'
    area_message = '//div[@class="_33LGR"]'
    # messages = "//span[@class='_3-8er selectable-text copyable-text']"

    unread = "_3C4Vf"
    unread_msg_no = "_1pJ9J"
    unread_contact_names = "zoWT4"
    msg_time = "_1beEj"
    # messages = "_1Gy50"
    messages = "_22Msk"
    # messages = "selectable-text copyable-text"

    @classmethod
    def start(cls):
        cls.chrome = webdriver.Chrome(executable_path=driver_location())
        cls.chrome.get(cls.wapweb)
        WebDriverWait(cls.chrome, 50000000).until(EC.presence_of_element_located((By.XPATH, cls.search_xpath)))

    def search(self,sender):
        search_box = self.chrome.find_element_by_xpath(self.search_xpath)
        search_box.clear()
        time.sleep(0.1)
        search_box.send_keys(sender)
        time.sleep(0.7)

        return self.chrome.find_element_by_xpath(self.sender_xpath)

    def send_message(self,sender,msg):
        sender_title = self.search(sender)

        try:
            sender_title.click()
        except:
            return "Sender's Name not found!"

        time.sleep(0.2)
        
        name = self.chrome.find_element_by_xpath(self.parent_xpath).text
        input_box = self.chrome.find_element_by_xpath(self.input_xpath)

        pyperclip.copy(msg)
        input_box.send_keys(Keys.SHIFT, Keys.INSERT)
        time.sleep(0.1)
        input_box.send_keys(Keys.ENTER)
        time.sleep(0.1)

        return name

    def read_message(self,unread_contact):
        data = [[] for i in range(3)]
        data[0].append(unread_contact.find_element(By.CLASS_NAME,self.unread_contact_names).text)

        try:
            number = int(unread_contact.find_element(By.CLASS_NAME,self.unread_msg_no).text)
        except:
            number = int((unread_contact.find_elements(By.CLASS_NAME,self.unread_msg_no)[1]).text)

        unread_contact.find_element(By.CLASS_NAME,self.unread_contact_names).click()
        time.sleep(0.5)

        # messages = self.chrome.find_elements_by_xpath(self.messages)
        area = self.chrome.find_element_by_xpath(self.area_message)

        for i in range(0,number/2):
            messages = area.find_elements(By.CLASS_NAME,self.messages)

            for message in messages:
                try:
                    data[1].append(message.text)
                except:
                    pass

            time.sleep(0.1)
            area.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

        return filter(data,number)

    def read_messages_individual(self,sender):
        return self.read_message(self.search(sender))

    def read_messages_all(self):
        data = []
        unread_contacts = self.chrome.find_elements(By.CLASS_NAME,self.unread)

        for unread_contact in unread_contacts:
            data.append(self.read_message(unread_contact))

        return data
    

@client.event
async def on_ready():

    print("Ready!")
    await client.change_presence(activity=discord.Game('X helpx'))
    Whatsapp.start()


@client.event
async def on_message(message):

    channel=message.channel
    wap=Whatsapp()

    if message.author == client.user:
        return
    else:
        inp=message.content.split()
        initial=inp[0].lower()
        com=inp[1].lower()

        if(initial=="x"):

            if(com=="helpx"):
                await channel.send(embed=discord.Embed(title= "Available Commands:\n", description= "send <sender's name> <message>\t\t-> it will push the link in the default channel\n\nshow", colour=discord.Colour.blue()))
            
            if(com=="send"):
                try:
                    sender=sender_msg(inp,2)[0]
                    msg=sender_msg(inp,2)[1]

                    try:
                        sender=wap.send_message(sender,msg)
                    except:
                        Whatsapp.start()
                        sender=wap.send_message(sender,msg)

                    if(sender=="Sender's Name not found!"):
                        await channel.send(embed=discord.Embed(title= "ERROR!\n", description= sender, colour=discord.Colour.red()))
                    else:
                        await channel.send(embed=discord.Embed(title= "Message Sent\n", description= "Sender: "+sender+"\nMessage: "+msg, colour=discord.Colour.blue()))
                
                except:
                    await channel.send(embed=discord.Embed(title= "ERROR!\n", description= "An unknown error has occured :(", colour=discord.Colour.red()))

            if(com=="scrap"):
                try:
                    limit=int(inp[2])
                    sender=sender_msg(inp,3)[0]
                    message = ""
                    c=0

                    async for msg in channel.history(limit=limit + 1000):
                        if msg.author != client.user:
                            if ((msg.content[0:6]).lower()!="x send" and (msg.content[0:7]).lower()!="x scrap"):
                                message += "*_" + msg.author.name + ":_* " + msg.content + "\n"
                                c+=1
                                if (c >= limit):
                                    break
                    
                    try:
                        wap.send_message(sender,message)
                    except:
                        Whatsapp.start()
                        wap.send_message(sender,message)
                        
                except:
                    await channel.send(embed=discord.Embed(title= "ERROR!\n", description= "Sender's name not found!", colour=discord.Colour.red()))

            if(com=="read"):
                unread_messages = ""

                if(len(inp)>=3):
                    sender=sender_msg(inp,2)[0]
                    try:
                        data=wap.read_messages_individual(sender)
                    except:
                        Whatsapp.start()
                        data=wap.read_messages_individual(sender)

                else:
                    try:
                        data=wap.read_messages_all()
                        print(data)
                    except:
                        Whatsapp.start()
                        data=wap.read_messages_all()
                        print(data)
                
                for i in range(0,len(data),3):
                    unread_messages += data[i] + "\n"

                    for j in range(1,len(data),3):
                        for k in range (0,len(data[j])):
                            unread_messages += '[' + data[j+1][k] + '] ' + data[j][k] + '\n'

                    unread_messages += "\n\n"

                if (unread_messages == ""):
                    unread_messages = "No unread messages!"

                await channel.send(embed=discord.Embed(title= "", description= unread_messages, colour=discord.Colour.red()))

#Call
#Send attatchments

if __name__=="__main__":
    client.run(Bot_Token)