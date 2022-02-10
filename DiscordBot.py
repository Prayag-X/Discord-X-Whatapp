from webbrowser import Chrome
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
from bs4 import BeautifulSoup

from Bot_Data import *
from Util import *

client=commands.Bot(command_prefix='')


class Whatsapp:

    chrome = None

    search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
    sender_xpath = '//span[@class="matched-text i0jNr"]'
    parent_xpath = '//span[.//span[@class="matched-text i0jNr"]]'
    input_xpath = '//div[@title="Type a message"]'
    area_message = '//div[@class="_33LGR"]'
    

    unread = "_3C4Vf"
    unread_contact_names = "zoWT4"
    messages = "selectable-text copyable-text"

    @classmethod
    def start(cls):
        cls.chrome = webdriver.Chrome(executable_path='D:/Programs/Discord X Whatsapp/chromedriver.exe')
        cls.chrome.get('https://web.whatsapp.com/')
        WebDriverWait(cls.chrome, 50000000).until(EC.presence_of_element_located((By.XPATH, cls.search_xpath)))

    def send_message(self,sender,msg):
        search_box = self.chrome.find_element_by_xpath(self.search_xpath)
        search_box.clear()
        time.sleep(0.1)
        search_box.send_keys(sender)
        time.sleep(0.7)

        try:
            sender_title = self.chrome.find_element_by_xpath(self.sender_xpath)
            sender_title.click()
            time.sleep(0.2)
        except:
            return "Sender's Name not found!"

        # soup = BeautifulSoup(self.chrome.page_source, "html.parser")
        # name=soup.find("span", class_="matched-text i0jNr").parent.text
        name=self.chrome.find_element_by_xpath(self.parent_xpath).text

        input_box = self.chrome.find_element_by_xpath(self.input_xpath)
        pyperclip.copy(msg)
        input_box.send_keys(Keys.SHIFT, Keys.INSERT)
        time.sleep(0.1)
        input_box.send_keys(Keys.ENTER)
        time.sleep(0.1)

        return name

    def read_messages(self,str=""):
        unread_names=[]
        msg=[]

        unread_contacts=self.chrome.find_elements(By.CLASS_NAME,self.unread)

        for unread_contact in unread_contacts:
            unread_names.append(unread_contact.find_element(By.CLASS_NAME,self.unread_contact_names).text)
        
        if(str=="names"):
            return unread_names
        
        for unread_contact in unread_contacts:
            unread_contact.find_element(By.CLASS_NAME,self.unread_contact_names).click()
            time.sleep(0.3)

            # area=self.chrome.find_element_by_xpath(self.area_message)
            # messages=self.chrome.find_elements(By.CLASS_NAME,self.messages)
            messages = self.chrome.find_elements_by_xpath("//span[@class='_3-8er selectable-text copyable-text']")

            for message in messages:
                msg.append(message.text)

            time.sleep(0.2)

        print (msg)
    
@client.event
async def on_ready():

    print("Yes Dragon X!")
    print("--------------")
    print(" ")

    await client.change_presence(activity=discord.Game('X helpx'))
    # Whatsapp.start()

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

        if(initial=="x" or initial=="urlx"):

            if(com=="helpx"):
                await channel.send(embed=discord.Embed(title= "Available Commands:\n", description= "send <sender's name> <message>\t\t-> it will push the link in the default channel\n\nshow", colour=discord.Colour.blue()))
            
            if(com=="send"):
                try:
                    sender_msg=util1(inp,2)
                    sender=sender_msg.split('|||')[0]
                    msg=sender_msg.split('|||')[1]

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
                    sender=util1(inp,3).split('|||')[0]
                    c=0

                    async for msg in channel.history(limit=limit + 1000):
                        if msg.author != client.user:
                            if ((msg.content[0:6]).lower()!="x send" and (msg.content[0:7]).lower()!="x scrap"):
                                message="*_"+msg.author.name+":_* "+msg.content
                                try:
                                    wap.send_message(sender,message)
                                except:
                                    Whatsapp.start()
                                    wap.send_message(sender,message)
                                c+=1
                                if (c >= limit):
                                    break

                except:
                    await channel.send(embed=discord.Embed(title= "ERROR!\n", description= "Sender's name not found!", colour=discord.Colour.red()))

            if(com=="read"):
                try:
                    print(wap.read_messages())
                except:
                    Whatsapp.start()
                    print(wap.read_messages())

#Read unread message and print it in discord
#Send attatchments

if __name__=="__main__":
    client.run(Bot_Token)