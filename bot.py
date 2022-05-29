import re
import time
import cloudscraper
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from os import environ
import aiohttp
from pyrogram import Client, filters

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
#API_KEY = environ.get('API_KEY')

bot = Client('LinkByPass bot',
             api_id= "1543212",
             api_hash= "d47de4b25ddf79a08127b433de32dc84",
             bot_token= "1814442638:AAEmIzweKsQ7HTZlp3vsfVT3UrXTt38aJkM")


@bot.on_message(filters.command('start'))
async def start(bot, message):
    await message.reply(
        f"**I Am Alive {message.chat.first_name}**\n"
        "**I Am Link Bypasser Bot, Just Send Me Short Link And Get Direct Link")

'''
@bot.on_message(filters.regex(r'\bhttps?://.*gplinks\.co\S+')))
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await gplinks_bypass(link)
        await message.reply(f'**Here Is Your Direct Link** : {short_link}', quote=True)
    except Exception as e:
        await message.reply(f'**Error** : {e}', quote=True)

@bot.on_message(filters.regex(r'\bhttps?://.*droplink\.co\S+'))
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await droplink_bypass(link)
        await message.reply(f'**Here Is Your Direct Link** : {short_link}', quote=True)
    except Exception as e:
        await message.reply(f'**Error** : {e}', quote=True)

   #await message.reply('**Link Correct ga Petu bro 🙂**')
'''

@bot.on_message(filters.regex(r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"))
async def link_handler(bot, message):
  link = message.matches[0].group(0)
  if 'gplinks.co' in link:
    try:
        short_link = await gplinks_bypass(link)
        await message.reply(f'**Here Is Your Direct Link** : {short_link}', quote=True)
    except Exception as e:
        await message.reply(f'**Error** : {e}', quote=True)
  elif 'droplink.co' in link:
     try:
        short_link = await droplink_bypass(link)
        await message.reply(f'**Here Is Your Direct Link** : {short_link}', quote=True)
     except Exception as e:
        await message.reply(f'**Error** : {e}', quote=True)
  else:
    pass

async def gplinks_bypass(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    res = client.head(url)
    header_loc = res.headers['location']
    param = header_loc.split('postid=')[-1]
    req_url = f'{p.scheme}://{p.netloc}/{param}'

    p = urlparse(header_loc)
    ref_url = f'{p.scheme}://{p.netloc}/'

    h = { 'referer': ref_url }
    res = client.get(req_url, headers=h, allow_redirects=False)

    bs4 = BeautifulSoup(res.content, 'html.parser')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'referer': ref_url,
        'x-requested-with': 'XMLHttpRequest',
    }
    time.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()['url'].replace('\/','/')
    except: 
        return "An Error Occured "

async def droplink_bypass(url):
    client = requests.Session()
    res = client.get(url)

    ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]

    h = {'referer': ref}
    res = client.get(url, headers=h)

    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest'
    }
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    time.sleep(3.1)
    res = client.post(final_url, data=data, headers=h)
    try:
        return res.json()['url'].replace('\/','/')
    except: 
        return "An Error Occured "
         



bot.run()
