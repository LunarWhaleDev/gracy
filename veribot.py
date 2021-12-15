# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import random
import logging
from time import sleep
import traceback
import sys
import requests
import json
import os
import os.path

from html import escape

from telegram import ParseMode, TelegramError, Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram.ext.dispatcher import run_async
#from telegram.contrib.botan import Botan
from engine import get_random_cats
from drinks import get_drink
#from binance.client import Client
import python3pickledb as pickledb

# Configuration
BOTNAME = 'GracyHope_bot'
TOKEN = 
#TOKEN = 
BOTAN_TOKEN = 'BOTANTOKEN'


help_text = 'Welcomes everyone that enters a group chat that this bot is a ' \
            'part of. By default, only the person who invited the bot into ' \
            'the group is able to change settings.\nCommands:\n\n' \
            '/setwelcome - Set welcome message\n' \
            '/setgoodbye - Set goodbye message\n' \
            '/disable\\_goodbye - Disable the goodbye message\n' \
            '/lock - Only the person who invited the bot can change messages\n' \
            '/unlock - Everyone can change messages\n' \
            '/quiet - Disable "Sorry, only the person who..." ' \
            '& help messages\n' \
            '/unquiet - Enable "Sorry, only the person who..." ' \
            '& help messages\n\n' \
            'You can use _$username_ and _$title_ as placeholders when setting' \
            ' messages. [HTML formatting]' \
            '(https://core.telegram.org/bots/api#formatting-options) ' \
            'is also supported. :) '
'''
Create database object
Database schema:
<chat_id> -> welcome message
<chat_id>_bye -> goodbye message
<chat_id>_adm -> user id of the user who invited the bot
<chat_id>_lck -> boolean if the bot is locked or unlocked
<chat_id>_quiet -> boolean if the bot is quieted

chats -> list of chat ids where the bot has received messages in.
'''
# Create database object

db = pickledb.load('bot.db', True)

if not db.get('chats'):
    db.set('chats', [])

# Set up logging
root = logging.getLogger()
root.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

db.set('disable_welcome', True)


@run_async
def send_async(bot, *args, **kwargs):
    bot.sendMessage(*args, **kwargs);


def check(bot, update, override_lock=None):
    """
    Perform some checks on the update. If checks were successful, returns True,
    else sends an error message to the chat and returns False.
    """

    chat_id = update.message.chat_id
    chat_str = str(chat_id)

    if chat_id > 0:
        send_async(bot, chat_id=chat_id,
                   text='Please add me to a group first!')
        return False

    locked = override_lock if override_lock is not None \
        else db.get(chat_str + '_lck')

    if locked and db.get(chat_str + '_adm') != update.message.from_user.id:
        if not db.get(chat_str + '_quiet'):
            send_async(bot, chat_id=chat_id, text='Sorry, only the person who '
                                                  'invited me can do that.')
        return False

    return True

def buy(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="VulcanDex:\nhttps://vulcandex.vulcanforged.com/#/swap?outputCurrency=0x348e62131fce2F4e0d5ead3Fe1719Bc039B380A9\n\nBinance:\nPYR-USDT\nhttps://www.binance.com/en/trade/PYR_USDT\nPYR-BTC\nhttps://www.binance.com/en/trade/PYR_BTC\n\nHuobi:\nhttps://www.huobi.com/en-us/exchange/pyr_usdt\n\nAscendex:\nhttps://ascendex.com/en/cashtrade-spottrading/usdt/pyr\n\nGate․io:\nhttps://www.gate.io/trade/PYR_USDT\n\nKucoin:\nPYR-BTC\nhttps://trade.kucoin.com/PYR-BTC\nPYR-USDT\nhttps://trade.kucoin.com/PYR-USDT\n\nBittrex:\nBTC-PYR\nhttps://global.bittrex.com/Market/Index?MarketName=BTC-PYR\nUSDT-PYR\nhttps://global.bittrex.com/Market/Index?MarketName=USDT-PYR\n\nQuickswap Polygon:\nhttps://info.quickswap.exchange/token/0x348e62131fce2f4e0d5ead3fe1719bc039b380a9\n\nUniswap Ethereum:\nhttps://app.uniswap.org/#/swap?outputCurrency=0x9534ad65fb398e27ac8f4251dae1780b989d136e&use=V2", disable_web_page_preview=True)

def sendvf(bot, update, args):
	text = " ".join(args)
	bot.sendMessage(chat_id=-1001294163207, text=text)
#	bot.sendMessage(chat_id=update.message.chat_id, text=update.message.chat_id)

def referral(bot, update):
	text = "Referrer = 50 $LAVA per new Vulcan wallet created.\nReferee = 10 $LAVA\n\nFind your Referral link in 'My Forge' Dash: http://myforge.vulcanforged.com\n\n*Lava is only claimable upon reaching 10k XP through gameplay.\nVulcanverse, Berserk, Forge Arena, BlockBabies and Battle Chess (playing speed chess mode)"
	bot.sendMessage(chat_id=update.message.chat_id, text=text)

def learn(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="https://vulcanforgedco.medium.com/\n\nCommunity made starter guide:\nhttps://docs.google.com/document/d/1p9ZI_pxFNoiqcz080YzY-rAGeUPB3JzPGtmYAIL1VNM/\n\nVisit the Vulcan-Classroom in https://discord.gg/vulcanverse")

def videos(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="How to create a myforge account:\nhttps://youtu.be/xh7QwEk7IvE\n\nBuying PYR and NFTs on the VulcanForged Marketplace:\nhttps://youtu.be/JDpNW9UeYps\n\nControls and UI Tutorial:\nhttps://youtu.be/osb7LU1wMnM\n\nHow to Forage and Build:\nhttps://youtu.be/JGq-uXsRc6U\n\nGame Footage:\nhttps://www.youtube.com/watch?v=W3SOw2Fio7A\nhttps://youtu.be/pxzOtShNMA8")

def reddit(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="https://www.reddit.com/r/VulcanForged/")

def twitter(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="https://twitter.com/vulcanforged")

def ronswanson(bot, update):
	r = requests.get('https://ron-swanson-quotes.herokuapp.com/v2/quotes')
	a = r.text
	bot.sendMessage(chat_id=update.message.chat_id, text=f"{a[2:-2]}\n-Ron Swanson")

def kanye(bot, update):
	r = requests.get('https://api.kanye.rest/?format=text')
	text = json.loads(r.text)
	bot.sendMessage(chat_id=update.message.chat_id, text=f"{text['quote']}\n-Kanye West")

def games(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Berserk\nhttps://berserk.vulcanforged.com\nhttps://bit.ly/3itsSie\nhttps://apple.co/3BdbYxb\n\nForge Arena\nhttps://arena.Vulcanforged.com\n\nBlockBabies\nhttps://blockbabies.world/play/\n\nChess\nhttps://chess.vulcanforged.com/\n\nCoddlePets\nhttps://rebrand.ly/dragongardenpc\nhttps://play.google.com/store/apps/details?id=com.coddlepets.dragongarden")

def tmcclardy(bot, update):
	headers = {
		'Accept': 'text/plain'
	}
	r = requests.get('https://icanhazdadjoke.com', headers=headers)
	bot.sendMessage(chat_id=update.message.chat_id, text=f"{r.text}\n-TMCCLARDY")

def joke(bot, update):
	r = requests.get('https://geek-jokes.sameerkumar.website/api?format=json')
	a = json.loads(r.text)
	bot.sendMessage(chat_id=update.message.chat_id, text=a['joke'])

def explosm(bot, update):
	url = "http://explosm.net/comics/"
	rnum = random.randint(5131,5621)
	imgurl = f"{url}{rnum}"
	bot.sendPhoto(chat_id=update.message.chat_id, photo=imgurl)

def nftmod(bot, update, args):
	user_id = update.message.chat_id
	tid = "".join(args)
	if not tid:
		text = "Please include the token id, and the commands.\nAcceptable commands are invert, grayscall, red, blue, green, and brown.\n\nExample: /nftmod 1 invert"
		bot.sendMessage(chat_id=update.message.chat_id, text=text)
		return
	api = f"http://api.vulcanforged.com/getArtByID/{args[0]}"
	r = requests.get(api)
	data = json.loads(r.text)
	td = data['data']
	ipfs = td['image']
	imageurl = f"https://cloudflare-ipfs.com/ipfs/{ipfs}"
	r = requests.get(imageurl, stream=True)
	if r.status_code != 200:
		bot.sendMessage(chat_id=user_id, text="Unable to load NFT")
		return
	open('input.jpeg', 'wb').write(r.content)
	text = "Attempting to modify the NFT image.\nMay take up to a minute."
	if args[1] == "invert":
		bot.sendMessage(chat_id=user_id, text=text)
		os.system('sudo python3 imageFilters/imageFilter.py --invert input.jpeg output.jpeg')
	elif args[1] == "grayscale":
		bot.sendMessage(chat_id=user_id, text=text)
		os.system('sudo python3 imageFilters/imageFilter.py --grayscale input.jpeg output.jpeg')
	elif args[1] == "red":
		bot.sendMessage(chat_id=user_id, text=text)
		os.system('sudo python3 imageFilters/imageFilter.py --color_filter --color red input.jpeg output.jpeg')
	elif args[1] == "blue":
		bot.sendMessage(chat_id=user_id, text=text)
		os.system('python3 imageFilters/imageFilter.py --color_filter --color blue input.jpeg output.jpeg')
	elif args[1] == "brown":
		bot.sendMessage(chat_id=user_id, text=text)
		os.system('python3 imageFilters/imageFilter.py --color_filter --color brown input.jpeg output.jpeg')
	elif args[1] == "green":
		bot.sendMessage(chat_id=user_id, text=text)
		os.system('python3 imageFilters/imageFilter.py --color_filter --color green input.jpeg output.jpeg')
	else:
		bot.sendMessage(chat_id=user_id, text="Incorrect mod argument.")
		return
	document2 = open('output.jpeg', 'rb')
	bot.sendPhoto(chat_id=user_id, photo=document2)

def meme(bot, update, args):
	tid = "".join(args)
	if not tid:
		text = "Please include the token id, and your text in the following format:\n/meme 0 making_nft/memes_now"
		bot.sendMessage(chat_id=update.message.chat_id, text=text)
		return
	api = f"http://api.vulcanforged.com/getArtByID/{args[0]}"
	r = requests.get(api)
	data = json.loads(r.text)
	td = data['data']
	ipfs = td['image']
	url1 = f"https://memegen.link/custom/{args[1]}.jpg?alt=https://cloudflare-ipfs.com/ipfs/{ipfs}"
	text = f"[Your NFT Meme:]({url1})"
#	bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN)
	bot.sendPhoto(chat_id=update.message.chat_id, photo=url1)

def nfttrack(bot, update, args):
	if not args:
		bot.sendMessage(chat_id=update.message.chat_id, text="Must include NFT id number.")
		return
	id = args[0]
	api = f"http://api.vulcanforged.com/getTrackOfArtById/{id}"
	r = requests.get(api)
	data = json.loads(r.text)
	info = data['data']
	text = "List of NFT owners in order:\n\n"
	for a in info:
		text = "".join((text, f"<code>{a}</code>\n\n"))
	bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode="HTML", disable_web_page_preview=True)

def nftraw(bot, update, args):
	if not args:
		bot.sendMessage(chat_id=update.message.chat_id, text="Must include NFT id number.")
		return
	id = args[0]
	api = f"http://api.vulcanforged.com/getArtByID/{id}"
	r = requests.get(api)
	data = json.loads(r.text)
	info = data['data']
	bot.sendMessage(chat_id=update.message.chat_id, text=info)

def nftid(bot, update, args):
	if not args:
		bot.sendMessage(chat_id=update.message.chat_id, text="Must include the NFT id number.")
		return
	id = args[0]
	api = f"http://api.vulcanforged.com/getArtByID/{id}"
	r = requests.get(api)
	data = json.loads(r.text)
	info = data['data']
	try:
		title = info['Name']
	except:
		try:
			title = info['Title']
		except:
			try:
				title = info['Plot']
			except:
				try:
					title = info['title']
				except:
						title = "Title Unknown"
	try:
		desc = info['Type']
	except:
		try:
			desc = info['Land']
		except:
			try:
				desc = info['Coordinates']
			except:
				try:
					desc = info['Description']
				except:
					try:
						desc = info['description']
					except:
						try:
							desc = f"\nTop: {info['Top']}\nLeft: {info['Left']}\nBottom: {info['Bottom']}\nRight: {info['Right']}"
						except:
							try:
								desc = info['Element']
							except:
								desc = "Description Unknown"
	try:
		author = info['author']
	except:
		author = "Author Unknown"
	owner = info['owner']
	if info['dappid'] == 7 or info['dappid'] == "7":
		try:
			desc = f"{desc}\nEdition: {info['Edition']}"
		except:
			desc = f"{desc}\nEdition: {info['Editions']}"
	if info['dappid'] == 4 or info['dappid'] == "4":
		desc = f"{desc}\nEdition: {info['Editions']}"
	try:
		image = info['image']
	except:
		image = "No image data"
#	ipfsurl = f"https://cloudflare-ipfs.com/ipfs/{image}"
	text = f"Title/Name: {title}\nDescription/Type: {desc}\nOwner: <code>{owner}</code>\nAuthor: <code>{author}</code>\nImage: <code>{image}</code>"
	bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode="HTML", disable_web_page_preview=True)
	if image == "No image data":
		return
	ipfsurl = f"https://cloudflare-ipfs.com/ipfs/{image}"
	r = requests.get(ipfsurl, stream=True)
	open('image.data', 'wb').write(r.content)
	with open('image.data','rb') as f:
		imagecontents = (f.read())
		if imagecontents.startswith(b'GIF'):
			bot.sendDocument(chat_id=update.message.chat_id, document=ipfsurl)
		else:
			bot.sendPhoto(chat_id=update.message.chat_id, photo=ipfsurl)

def nftaddress(bot, update, args):
	if not args:
		bot.sendMessage(chat_id=update.message.chat_id, text="Must include address after command.")
		return
	address = args[0].lower()
	api = f"http://api.vulcanforged.com/tokensOfOwner/{address}"
	r = requests.get(api)
	data = json.loads(r.text)
	tokens = data['data']
	text = f"<code>{address}</code>:\n\n"
	for a in tokens:
		text = "".join((text, f"#{a}, "))
	text = f"{text[:-2]}\n\nFetching titles (May take a few minutes):"
	try:
		bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode="HTML", disable_web_page_preview=True)
	except:
		bot.sendMessage(chat_id=update.message.chat_id, text="Message too long for Telegram.")
		return
	text = f"<code>{address}</code>:\n\n"
	sent = bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode="HTML", disable_web_page_preview=True)
#	bot.sendMessage(chat_id=update.message.chat_id, text=sent.message_id)
	for a in tokens:
		tokenapi = f"http://api.vulcanforged.com/getArtByID/{a}"
		r = requests.get(tokenapi)
		data = json.loads(r.text)
		info = data['data']
		try:
			title = info['Name']
		except:
			try:
				title = info['Title']
			except:
				try:
					title = f"Land Plot: {info['Plot']}"
				except:
					try:
						title = info['title']
					except:
						title = "Title Unknown"
		text = "".join((text, f"#{a}: {title}\n"))
		try:
			bot.edit_message_text(chat_id=update.message.chat_id, message_id=sent.message_id, text=text, parse_mode="HTML", disable_web_page_preview=True)
		except:
			bot.sendMessage(chat_id=update.message.chat_id, text="Message too long for telegram.")
			return

#		print(text)
#		text = f"#{a}: {info['title']}"
#	bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode="HTML", disable_web_page_preview=True)

#def power(bot, update):
#	text = "Vulcan Forged will be powering at least 10 dApps this year with the number growing. Here’s a summary of confirmed NFT applications using our engine:\n\nhttps://medium.com/@vulcanforgedco/vulcan-forged-10-dapps-coming-in-2020-715e79b94caa"
#	bot.sendMessage(chat_id=update.message.chat_id, text=text)

#def binance(bot, update, args):
#	argtest = "".join(args)
#	if not argtest:
#		bot.sendMessage(chat_id=update.message.chat_id, text="Please enter one ticker pair after the command /binance\nExample: /binance vetbtc")
#		return
#	prices = client.get_all_tickers()
#	input = args[0]
#	coin = input.upper()
#	for a in prices:
#		if a['symbol'] == coin:
#			bot.sendMessage(chat_id=update.message.chat_id, text=("Price of "+coin+" on Binance is "+a['price']))

#def oceanex(bot, update, args):
#	user_id=update.message.chat_id
#	ticker = "".join(args)
#	if not ticker:
#		bot.sendMessage(chat_id=user_id, text="Please send any ticker pair after the /oceanex command.\nExample: /oceanex vetbtc veteth")
#		return
#	base_url = "https://api.oceanex.pro/v1/tickers_multi"
#	markets = args
#	data = {
#	 "markets[]": markets
#	}
#	r = requests.post(base_url, data=data)
#	output = json.loads(r.text)
#	tickers = output['data']
#	for a in tickers:
#		td = a['ticker']
#		text = f"Ticker Pair: {a['market']}\nLast Price: {td['last']}\n\nBid: {td['buy']}\nAsk: {td['sell']}\nLow: {td['low']}\nHigh: {td['high']}\nVolume: {td['vol']}"
#		bot.sendMessage(chat_id=user_id, text=text)

def marketplace(bot, update):
#	bot.sendMessage(chat_id=update.message.chat_id, text="https://market.vulcanforged.com/")
	bot.sendMessage(chat_id=update.message.chat_id, text=("https://market.vulcanforged.com/\n\nThe Vulcan Forged marketplace is the first multi-dApp NFT marketplace. Buy, sell and bid on NFTs from a variety of VulcanForged dApps. Here is a video with the basics:\nhttps://www.youtube.com/watch?v=JDpNW9UeYps&list=PLchjiGFQDIl4fdzlVM1U0--Z93RK6qcwD&index=3"))

def discord(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="https://Discord.gg/VulcanVerse")

def report(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="Reported.")
  bot.sendMessage(chat_id=393501230, text="Reported message.")
  bot.sendMessage(chat_id=372535389, text="Reported message.")
  bot.sendMessage(chat_id=537130951, text="Reported message.")
  bot.sendMessage(chat_id=303651782, text="Reported message.")

def drink(bot, update, args):
  if not args:
    bot.sendMessage(chat_id=update.message.chat_id, text="Please specify drink.")
  if args[0] == "random":
    api = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
  else:
    drink = "_".join(args)
    api = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}"
  r = requests.get(api)
  jsondata = json.loads(r.text)
  rdrink = jsondata['drinks']
  data = rdrink[0]
  text = f"Drink Name: {data['strDrink']}\nType: {data['strCategory']} / {data['strAlcoholic']}\nGlass: {data['strGlass']}\n\nInstructions:\n{data['strInstructions']}\n"
  if data['strMeasure1'] is None:
    m1 = ""
  else:
    m1 = f"{data['strMeasure1']} "
  if data['strIngredient1'] is None:
    i1 = ""
  else:
    i1 = f"{data['strIngredient1']}\n"
  if data['strMeasure2'] is None:
    m2 = ""
  else:
    m2 = f"{data['strMeasure2']} "
  if data['strIngredient2'] is None:
    i2 = ""
  else:
    i2 = f"{data['strIngredient2']}\n"
  if data['strMeasure3'] is None:
    m3 = ""
  else:
    m3 = f"{data['strMeasure3']} "
  if data['strIngredient3'] is None:
    i3 = ""
  else:
    i3 = f"{data['strIngredient3']}\n"
  if data['strMeasure4'] is None:
    m4 = ""
  else:
    m4 = f"{data['strMeasure4']} "
  if data['strIngredient4'] is None:
    i4 = ""
  else:
    i4 = f"{data['strIngredient4']}\n"
  if data['strMeasure5'] is None:
    m5 = ""
  else:
    m5 = f"{data['strMeasure5']} "
  if data['strIngredient5'] is None:
    i5 = ""
  else:
    i5 = f"{data['strIngredient5']}\n"
  if data['strMeasure6'] is None:
    m6 = ""
  else:
   m6 = f"{data['strMeasure6']} "
  if data['strIngredient6'] is None:
    i6 = ""
  else:
    i6 = f"{data['strIngredient6']}\n"
  if data['strMeasure7'] is None:
    m7 = ""
  else:
    m7 = f"{data['strMeasure7']} "
  if data['strIngredient7'] is None:
    i7 = ""
  else:
    i7 = f"{data['strIngredient7']}\n"
  if data['strMeasure8'] is None:
    m8 = ""
  else:
    m8 = f"{data['strMeasur81']} "
  if data['strIngredient8'] is None:
    i8 = ""
  else:
    i8 = f"{data['strIngredient8']}\n"
  if data['strMeasure9'] is None:
    m9 = ""
  else:
    m9 = f"{data['strMeasure9']} "
  if data['strIngredient9'] is None:
    i9 = ""
  else:
    i9 = f"{data['strIngredient9']}\n"
  if data['strMeasure10'] is None:
    m10 = ""
  else:
    m10 = f"{data['strMeasure10']} "
  if data['strIngredient10'] is None:
    i10 = ""
  else:
    i10 = f"{data['strIngredient10']}\n"
  if data['strMeasure11'] is None:
    m11 = ""
  else:
    m11 = f"{data['strMeasure11']} "
  if data['strIngredient11'] is None:
    i11 = ""
  else:
    i11 = f"{data['strIngredient11']}\n"
  if data['strMeasure12'] is None:
    m12 = ""
  else:
    m12 = f"{data['strMeasure12']} "
  if data['strIngredient12'] is None:
    i12 = ""
  else:
    i12 = f"{data['strIngredient12']}\n"
  if data['strMeasure13'] is None:
    m13 = ""
  else:
    m13 = f"{data['strMeasure13']} "
  if data['strIngredient13'] is None:
    i13 = ""
  else:
    i13 = f"{data['strIngredient13']}\n"
  if data['strMeasure14'] is None:
    m14 = ""
  else:
    m14 = f"{data['strMeasure14']} "
  if data['strIngredient14'] is None:
    i14 = ""
  else:
    i14 = f"{data['strIngredient14']}\n"
  if data['strMeasure15'] is None:
    m15 = ""
  else:
    m15 = f"{data['strMeasure15']} "
  if data['strIngredient15'] is None:
    i15 = ""
  else:
    i15 = f"{data['strIngredient15']}\n"
  text2 = f"{m1}{i1}{m2}{i2}{m3}{i3}{m4}{i4}{m5}{i5}{m6}{i6}{m7}{i7}{m8}{i8}{m9}{i9}{m10}{i10}{m11}{i11}{m12}{i12}{m13}{i13}{m14}{i14}{m15}{i15}"
  mtext = "".join((text, text2))
  bot.sendMessage(chat_id=update.message.chat_id, text=mtext)
  bot.sendPhoto(chat_id=update.message.chat_id, photo=data['strDrinkThumb'])

def cats(bot, update):
        bot.sendDocument(chat_id=update.message.chat_id, document=get_random_cats())

def info(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=("Hi! Send any of the following commands to receive more information!\n\n/rules\n/learn\n/buy\n/marketplace\n/games\n/discord\n/reddit\n/twitter\n/buynfts\n/import\n/lava\n/videos\n/vulcanverse\n/wayofthetiger\n/blockbabies\n/geocats\n/stamp\n/rektcity\n/nftid\n/nftaddress\n/meme\n/nftmod\n/nfttrack\n/nftraw\n/report"))

#def landsale(bot, update):
#	bot.sendMessage(chat_id=update.message.chat_id, text="https://vulcanverse.com/vulcanverse-land-sale-guide/")
#	bot.sendMessage(chat_id=update.message.chat_id, text="https://vulcanverse.com/test/")

def rektcity(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=("@RektCity_bot\n\nA mobile game on Telegram that uses Veriarti NFTs, powered by VulcanForged\n\nWage war on the city and establish dominance. Do you have what it takes to become Kingpin?\n\nhttps://twitter.com/rekt_city_game"))

def rules(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=("VulcanForged - Marketplace and hub for NFTs and dApps built on the VulcanForged platform\n\nRules: Pretty chilled, talk about anything Vulcan Forged and Vulcan projects, just don't be offensive or bring drama from other groups!\n\nWebsite: https://market.vulcanforged.com"))

def import_(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="https://vulcanforgedco.medium.com/switching-to-pyr-101-a-guide-a813a82ea49c")

#def veriarti(bot, update):
#	bot.sendMessage(chat_id=update.message.chat_id, text=("VeriArti - Unique digital art tokens (NFTs) on the leading enterprise blockchain"))

#def vulcan(bot, update):
#	bot.sendMessage(chat_id=update.message.chat_id, text=("Vulcan - Marketplace and hub for NFTs and dApps built on VeChainThor"))

def nft(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=("NFT stands for Non-Fungible Token. It is essentially a unique digital token on the blockchain that can never be deleted or copied. It provides the ability to give the same rarity to digital items as you would physical."))

#def vechainrocket(bot, update):
#	bot.sendMessage(chat_id=update.message.chat_id, text=("Burn VTHO. Win Prizes.\n\n#VechainRocket\nhttps://vthorium.com\n\nThe VulcanX VThorium takes VTHO as fuel. 500 million VTHO will power it to the moon. As you burn your VTHO to fuel it, pick up prizes at various altitudes. Anyone can add a prize."))

def vulcanverse(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="VulcanVerse is an AAA decentralized fantasy world based in the Greco-Roman era, backed by Fighting Fantasy authors with MMO functionality\nhttps://vv.vulcanforged.com/")

def blockbabies(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=("https://medium.com/@blockbabiesofficial/block-babies-decentralised-infant-chaos-7267e46abaf1"))

def buynfts(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="https://market.vulcanforged.com/\n\nTo interact with the Marketplace (auctions,trades etc) you must first move PYR from 'Main Wallet' to 'Market Wallet'")

def geocats(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=("https://medium.com/@geocats/geocats-codex-1-87fd5676cc49"))

def stamp(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=("https://medium.com/@jamiesinbox/introducing-stamp-veriartis-ip-flagship-product-58c0f4e8038"))

def lava(bot, update):
	text = (
		"https://vulcanforgedco.medium.com/lava-gems-multiplier-program-update-84890869e36f\n\n"
		"Lava Token Contract:\n"
		"0xb4666B7402D287347DbBDC4EA5b30E80C376c0B3\n\n"
		"Upgrading Land\n"
		"Purchasing consumables in-game\n"
		"Upgrade Vulcanite stats\n"
		"Activate NFT seeds\n"
		"Unlocking game features in different Vulcan Forged games\n"
		"Staking in VulcanDex\n"
		"Purchasing in-game assets\n"
		"Upgrade Gods\n"
		"Enter Tournaments\n\n"
		"Fees:\n"
		"Seed activation fees\n"
		"Land upgrade fees\n"
		"Upgrading Vulcanites\n"
		"Upgrading and Maintaining Titans and Olympians\n\n"
		"Burn: Every single lava expenditure route is a 100% burn such as:\n\n"
		"All seed activation costs\n"
		"Fees for upgrading Vulcanites\n"
		"All god upgrade and maintenance fees\n"
		"All land upgrade fees\n"
		"Purchasing consumables in-game via NPCs"
		)

	bot.sendMessage(chat_id=update.message.chat_id, text=text)

# Welcome a user to the chat
def welcome(bot, update):
    """ Welcomes a user to the chat """

    message = update.message
    chat_id = message.chat.id
    logger.info('%s joined to chat %d (%s)'
                 % (escape(message.new_chat_member.first_name),
                    chat_id,
                    escape(message.chat.title)))

    if db.get('disable_welcome') == True:
      return


    # Pull the custom message for this chat from the database
    text = db.get(str(chat_id))

    # Use default message if there's no custom one set
    if text is None:
        text = 'Hello $username! Welcome to $title'

    # Replace placeholders and send message
    text = text.replace('$username',
                        message.new_chat_member.first_name)\
        .replace('$title', message.chat.title)
    send_async(bot, chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)

    rnum = random.randint(1,17)
    if rnum == 1:
      tid = 10430
    if rnum == 2:
      tid = 14897
    if rnum == 3:
      tid = 14934
    if rnum == 4:
      tid = 15234
    if rnum == 5:
      tid = 31061
    if rnum == 6:
      tid = 31749
    if rnum == 7:
      tid = 13801
    if rnum == 8:
      tid = 28859
    if rnum == 9:
      tid = 15607
    if rnum == 10:
      tid = 34772
    if rnum == 11:
      tid = 16219
    if rnum == 12:
      tid = 15161
    if rnum == 13:
      tid = 28687
    if rnum == 14:
      tid = 15450
    if rnum == 15:
      tid = 32084
    if rnum == 16:
      tid = 32239
    if rnum == 17:
      tid = 32773
    tokenurl = f"http://api.vulcanforged.com/getArtByID/{tid}"
    r = requests.get(tokenurl)
    data = json.loads(r.text)
    td = data['data']
    ipfs = td['image']
    url1 = f"https://memegen.link/custom/welcome_to/vulcan.jpg?alt=https://cloudflare-ipfs.com/ipfs/{ipfs}"
    text = f"Here is a random NFT on the blockchain with your welcome message: [Number {tid}](https://cloudflare-ipfs.com/ipfs/{ipfs})"
    bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=url1)

# Welcome a user to the chat
def goodbye(bot, update):
    """ Sends goodbye message when a user left the chat """

    message = update.message
    chat_id = message.chat.id
    logger.info('%s left chat %d (%s)'
                 % (escape(message.left_chat_member.first_name),
                    chat_id,
                    escape(message.chat.title)))

    # Pull the custom message for this chat from the database
    text = db.get(str(chat_id) + '_bye')

    # Goodbye was disabled
    if text is False:
        return

    # Use default message if there's no custom one set
    if text is None:
        text = 'Goodbye, $username!'

    # Replace placeholders and send message
    text = text.replace('$username',
                        message.left_chat_member.first_name)\
        .replace('$title', message.chat.title)
    bot.sendMessage(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)

#    imgurl = "https://memegen.link/custom/see_ya/nerd.jpg?alt=https://cloudflare-ipfs.com/ipfs/QmNuZdQmsVXt63CcAwcm8d7gPDXdrvYeXEzBHBgdMb88yH"
#    bot.sendPhoto(chat_id=update.message.chat_id, photo=imgurl)

# Introduce the bot to a chat its been added to
def introduce(bot, update):
    """
    Introduces the bot to a chat its been added to and saves the user id of the
    user who invited us.
    """

    chat_id = update.message.chat.id
    invited = update.message.from_user.id

    logger.info('Invited by %s to chat %d (%s)'
                % (invited, chat_id, update.message.chat.title))

    db.set(str(chat_id) + '_adm', invited)
    db.set(str(chat_id) + '_lck', True)

    text = 'Hello! I will now greet anyone who joins this chat with a nice message!\nCheck the /welcomehelp command for more info!'
    send_async(bot, chat_id=chat_id, text=text)


# Print help text
def help(bot, update):
    """ Prints help text """

    chat_id = update.message.chat.id
    chat_str = str(chat_id)
    if (not db.get(chat_str + '_quiet') or db.get(chat_str + '_adm') ==
            update.message.from_user.id):
        send_async(bot, chat_id=chat_id,
                   text=help_text,
                   parse_mode=ParseMode.MARKDOWN,
                   disable_web_page_preview=True)


# Set custom message
def set_welcome(bot, update, args):
    """ Sets custom welcome message """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(bot, update):
        return

    # Split message into words and remove mentions of the bot
    message = ' '.join(args)

    # Only continue if there's a message
    if not message:
        send_async(bot, chat_id=chat_id, 
                   text='You need to send a message, too! For example:\n'
                        '<code>/setwelcome Hello $username, welcome to '
                        '$title!</code>',
                   parse_mode=ParseMode.HTML)
        return

    # Put message into database
    db.set(str(chat_id), message)

    send_async(bot, chat_id=chat_id, text='Got it!')


# Set custom message
def set_goodbye(bot, update, args):
    """ Enables and sets custom goodbye message """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(bot, update):
        return

    # Split message into words and remove mentions of the bot
    message = ' '.join(args)

    # Only continue if there's a message
    if not message:
        send_async(bot, chat_id=chat_id, 
                   text='You need to send a message, too! For example:\n'
                        '<code>/setgoodbye Goodbye, $username!</code>',
                   parse_mode=ParseMode.HTML)
        return

    # Put message into database
    db.set(str(chat_id) + '_bye', message)

    send_async(bot, chat_id=chat_id, text='Got it!')


def disable_goodbye(bot, update):
    """ Disables the goodbye message """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(bot, update):
        return

    # Disable goodbye message
    db.set(str(chat_id) + '_bye', False)

    send_async(bot, chat_id=chat_id, text='Got it!')


def lock(bot, update):
    """ Locks the chat, so only the invitee can change settings """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(bot, update, override_lock=True):
        return

    # Lock the bot for this chat
    db.set(str(chat_id) + '_lck', True)

    send_async(bot, chat_id=chat_id, text='Got it!')


def quiet(bot, update):
    """ Quiets the chat, so no error messages will be sent """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(bot, update, override_lock=True):
        return

    # Lock the bot for this chat
    db.set(str(chat_id) + '_quiet', True)

    send_async(bot, chat_id=chat_id, text='Got it!')


def unquiet(bot, update):
    """ Unquiets the chat """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(bot, update, override_lock=True):
        return

    # Lock the bot for this chat
    db.set(str(chat_id) + '_quiet', False)

    send_async(bot, chat_id=chat_id, text='Got it!')


def unlock(bot, update):
    """ Unlocks the chat, so everyone can change settings """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(bot, update):
        return

    # Unlock the bot for this chat
    db.set(str(chat_id) + '_lck', False)

    send_async(bot, chat_id=chat_id, text='Got it!')


def empty_message(bot, update):
    """
    Empty messages could be status messages, so we check them if there is a new
    group member, someone left the chat or if the bot has been added somewhere.
    """

    # Keep chatlist
    chats = db.get('chats')

    if update.message.chat.id not in chats:
        chats.append(update.message.chat.id)
        db.set('chats', chats)
        logger.info("I have been added to %d chats" % len(chats))

    if update.message.new_chat_member is not None:
        # Bot was added to a group chat
        if update.message.new_chat_member.username == BOTNAME:
            return introduce(bot, update)
        # Another user joined the chat
        else:
            return welcome(bot, update)

    # Someone left the chat
    elif update.message.left_chat_member is not None:
        if update.message.left_chat_member.username != BOTNAME:
            return goodbye(bot, update)



def error(bot, update, error, **kwargs):
    """ Error handling """

    try:
        if isinstance(error, TelegramError)\
                and error.message == "Unauthorized"\
                or "PEER_ID_INVALID" in error.message\
                and isinstance(update, Update):

            chats = db.get('chats')
            chats.remove(update.message.chat_id)
            db.set('chats', chats)
            logger.info('Removed chat_id %s from chat list'
                        % update.message.chat_id)
        else:
            logger.error("An error (%s) occurred: %s"
                         % (type(error), error.message))
    except:
        pass


botan = None
if BOTAN_TOKEN != 'BOTANTOKEN':
    botan = Botan(BOTAN_TOKEN)

@run_async
def stats(bot, update, **kwargs):
    if not botan:
        return

    if botan.track(update.message):
        logger.debug("Tracking with botan.io successful")
    else:
        logger.info("Tracking with botan.io failed")


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=False)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("learn", learn))
    dp.add_handler(CommandHandler("videos", videos))
    dp.add_handler(CommandHandler("discord", discord))
    dp.add_handler(CommandHandler("reddit", reddit))
    dp.add_handler(CommandHandler("twitter", twitter))
    dp.add_handler(CommandHandler("ronswanson", ronswanson))
    dp.add_handler(CommandHandler("kanye", kanye))
    dp.add_handler(CommandHandler("tmcclardy", tmcclardy))
    dp.add_handler(CommandHandler("joke", joke))
    dp.add_handler(CommandHandler("rektcity", rektcity))
    dp.add_handler(CommandHandler("explosm", explosm))
    dp.add_handler(CommandHandler("nftmod", nftmod, pass_args=True))
    dp.add_handler(CommandHandler("meme", meme, pass_args=True))
    dp.add_handler(CommandHandler("nfttrack", nfttrack, pass_args=True))
    dp.add_handler(CommandHandler("nftraw", nftraw, pass_args=True))
    dp.add_handler(CommandHandler("nftid", nftid, pass_args=True))
    dp.add_handler(CommandHandler("nftaddress", nftaddress, pass_args=True))
#    dp.add_handler(CommandHandler("power", power))
    dp.add_handler(CommandHandler("marketplace", marketplace))
#    dp.add_handler(CommandHandler("binance", binance, pass_args=True))
#    dp.add_handler(CommandHandler("oceanex", oceanex, pass_args=True))
    dp.add_handler(CommandHandler("drink", drink, pass_args=True))
    dp.add_handler(CommandHandler("cats", cats))
    dp.add_handler(CommandHandler("info", info))
#    dp.add_handler(CommandHandler("landsale", landsale))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("import", import_))
#    dp.add_handler(CommandHandler("veriarti", veriarti))
#    dp.add_handler(CommandHandler("vulcan", vulcan))
    dp.add_handler(CommandHandler("nft", nft))
    dp.add_handler(CommandHandler("buy", buy))
    dp.add_handler(CommandHandler("report", report))
    dp.add_handler(CommandHandler("sendvf", sendvf, pass_args=True))
 #   dp.add_handler(CommandHandler("vechainrocket", vechainrocket))
    dp.add_handler(CommandHandler("vulcanverse", vulcanverse))
    dp.add_handler(CommandHandler("buynfts", buynfts))
    dp.add_handler(CommandHandler("blockbabies", blockbabies))
    dp.add_handler(CommandHandler("geocats", geocats))
    dp.add_handler(CommandHandler("stamp", stamp))
    dp.add_handler(CommandHandler("lava", lava))
    dp.add_handler(CommandHandler("games", games))
    dp.add_handler(CommandHandler("pyr", buy))
    dp.add_handler(CommandHandler("referral", referral))
    dp.add_handler(CommandHandler("welcomehelp", help))
    dp.add_handler(CommandHandler('setwelcome', set_welcome, pass_args=True))
    dp.add_handler(CommandHandler('setgoodbye', set_goodbye, pass_args=True))
    dp.add_handler(CommandHandler('disable_goodbye', disable_goodbye))
    dp.add_handler(CommandHandler("lock", lock))
    dp.add_handler(CommandHandler("unlock", unlock))
    dp.add_handler(CommandHandler("quiet", quiet))
    dp.add_handler(CommandHandler("unquiet", unquiet))

    dp.add_handler(MessageHandler(Filters.status_update, empty_message))
    dp.add_handler(MessageHandler(Filters.text, stats))

    dp.add_error_handler(error)

    update_queue = updater.start_polling(timeout=30, clean=False)

    updater.idle()

if __name__ == '__main__':
    main()
