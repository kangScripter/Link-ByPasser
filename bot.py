import time
import cloudscraper
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from os import environ
import aiohttp
from pyrogram import Client, filters

API_ID = 5540967 #environ.get('API_ID')
API_HASH = "eedf0196b0533f361b51b5b7082358e9"#environ.get('API_HASH')
BOT_TOKEN = "1814442638:AAEmIzweKsQ7HTZlp3vsfVT3UrXTt38aJkM"#environ.get('BOT_TOKEN')
#API_KEY = environ.get('API_KEY')

bot = Client('gplink bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN)



@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm GPlink bot. Just send me link and get short link")


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await gplinks_bypass(link)
        await message.reply(f'Here is your {short_link}', quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)



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
            
         


bot.run()
