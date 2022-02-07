import telebot
import config
import requests
import datetime
from datetime import date
from datetime import timedelta
import time
from bs4 import BeautifulSoup
from telebot import types
import json


def reqRate(symbol):
    response = requests.get("https://data.messari.io/api/v1/assets/"+ symbol +"/metrics", headers = config.HEADERS)
    response = json.loads(response.text)
    price = round(response['data']['market_data']['price_usd'], 2)
    return price
    
def getDisResponse(id):
    response = requests.get('https://discord.com/api/v8/invites/'+id+'?with_counts=true', headers = config.HEADERS)
    return response.json()

# def createDropMessageContent(row):

#     dropDate = datetime.datetime.strptime(row['Date'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=3)
#     dropDate = dropDate.strftime("%d/%m/%Y %H:%M")

#     markup = types.InlineKeyboardMarkup(row_width=2)
    
#     if row['TwitLink'] != None: 
#         markup.add(types.InlineKeyboardButton(text='Twitter', url=row['TwitLink']))

#     if row['DisLink'] != None: 
#         markup.add(types.InlineKeyboardButton(text='Discord', url=row['DisLink']))

#     if row['DisLink'] != None: 
#         disResponse = getDisResponse(str(row['DisLink']).split("/")[-1])
#         if disResponse['code'] != 10006:
#             disOnline = str(disResponse['approximate_presence_count'])
#             disMember = str(disResponse['approximate_member_count'])
#         else:
#             disOnline = 'None'
#             disMember = 'None'

#     imgSrc = row['ImgSrc']

#     text =  f"📛 Имя:     "+ str(row['Title'])   +"\n" \
#             f"📅 Дата:    "+ str(dropDate)       +"\n\n" \
#             f"👥 Discord: "+ disMember      +"\n" \
#             f"🟢 Online:  "+ disOnline      +"\n\n" \
#             f"🐦 Twitter: "+ str(row['TwitFol']) +"\n\n" \
#             f"🪙 Цена:    "+ str(row['Price'])  +"\n" \
#             f"📦 Кол-во:  "+ str(row['Items'])
    
#     return {'textMessage': text, 'imgSrc': imgSrc ,'markup': markup}

def createDropMessageContent(drop):
    markup = types.InlineKeyboardMarkup(row_width=2)

    dropDate = drop['date']
    imgSrc = drop['image']
    
    if drop['twitter'] != None: 
        markup.add(types.InlineKeyboardButton(text='Twitter', url=drop['twitter']))
    if drop['discord'] != None: 
        markup.add(types.InlineKeyboardButton(text='Discord', url=drop['discord']))
    if drop['discord'] != None: 
        disResponse = getDisResponse(str(drop['discord']).split("/")[-1])
        if disResponse['code'] != 10006:
            disOnline = str(disResponse['approximate_presence_count'])
            disMember = str(disResponse['approximate_member_count'])
        else:
            disOnline = 'None'
            disMember = 'None'
    text =  f"📛 Имя:     "+ drop['name']   +"\n" \
        f"📅 Дата:    "+ dropDate       +"\n\n" \
        f"👥 Discord: "+ disMember      +"\n" \
        f"🟢 Online:  "+ disOnline      +"\n\n" \
        f"🪙 Цена:    "+ drop['price']  +"\n" \
        f"📦 Кол-во:  "+ str(drop['nft_count'])

    
    return {'textMessage': text, 'imgSrc': imgSrc ,'markup': markup}


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📈 Курс SOL","📈 Курс ETH")
    markup.row("🗓️ Дропы Solana на сегодня")
    markup.row("📅 Все дропы Solana")

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n Я - {1.first_name}, твой личный помощник в мире NFT".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handler(message):
    if message.chat.type == 'private':
        if message.text == "📈 Курс SOL":
            bot.send_message(message.chat.id, "SOL= " + str(reqRate('sol'))+"$")
        if message.text == "📈 Курс ETH":
            bot.send_message(message.chat.id, "ETH= " + str(reqRate('eth'))+"$")
        if message.text == "🗓️ Дропы Solana на сегодня":
            with open('solDrop.json') as file:
                drops = json.load(file)
                drops = drops['result']['data'][str(date.today())]

            for drop in drops:
                messageContent = createDropMessageContent(drop)
                bot.send_photo(message.chat.id, drop['image'], caption= messageContent['textMessage'], parse_mode="HTML", reply_markup=messageContent['markup'])


        if message.text == "📅 Все дропы Solana":
            with open('solDrop.json') as file:
                drops = json.load(file)

            drops = pd.read_csv(config.ETHDROPDATA ,sep='\t')
            for index, row in drops.iterrows():
                messageContent = createDropMessageContent(row)
                bot.send_photo(message.chat.id, messageContent['imgSrc'], caption= messageContent['textMessage'], parse_mode="HTML", reply_markup=messageContent['markup'])

bot.polling(none_stop=True)