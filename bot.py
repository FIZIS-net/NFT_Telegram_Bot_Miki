import telebot
import config
import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from telebot import types

def rateParser(url):
    response = requests.get(url, headers = config.HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    rate = soup.find('span', {"id": "last_last"}).text
    return rate

def getDisResponse(id):
    response = requests.get('https://discord.com/api/v8/invites/'+id+'?with_counts=true', headers = config.HEADERS)
    return response.json()

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📈 Курс SOL","📈 Курс ETH")
    markup.row("📅 Дропы на Solana")
    markup.row("📅 Дропы на Ethereum")

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n Я - {1.first_name}, твой личный помощник в мире NFT".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handler(message):
    if message.chat.type == 'private':
        if message.text == "📈 Курс SOL":
            bot.send_message(message.chat.id, "SOL= " + rateParser(config.SOLRATEURL)+"$")
        if message.text == "📈 Курс ETH":
            bot.send_message(message.chat.id, "ETH= " + rateParser(config.ETHRATEURL)+"$")
        if message.text == "📅 Дропы на Solana":
            drops = pd.read_csv(config.SOLDROPDATA ,sep='\t')
            for index, row in drops.iterrows():
                markup = types.InlineKeyboardMarkup(row_width=2)
                
                if row['TwitLink'] != '0' and row['TwitLink'] != None: 
                    markup.row(types.InlineKeyboardButton(text='Twitter', url=row['TwitLink']))

                if row['DisLink'] != '0' and row['DisLink'] != None and row['DisLink'] != 'none': 
                    markup.row(types.InlineKeyboardButton(text='Discord', url=row['DisLink']))


                if row['DisLink'] != '0' and row['DisLink'] != None and row['DisLink'] != 'none': 
                    disResponse = getDisResponse(row['DisLink'].split("/")[-1])
                    disOnline = str(disResponse['approximate_presence_count'])
                    disMember = str(disResponse['approximate_member_count'])
                else:
                    disOnline = 'undefiend'
                    disMember = 'undefiend'

                text =  f"📛 Имя:     "+ row['Title']   +"\n" \
                        f"📅 Дата:    "+ str(datetime.datetime.strptime(row['Date'], "%Y-%m-%dT%H:%M:%SZ"))+"\n\n" \
                        f"👥 Discord: "+ disMember      +"\n" \
                        f"🟢 Online:  "+ disOnline      +"\n\n" \
                        f"🐦 Twitter: "+ row['TwitFol'] +"\n\n" \
                        f"🪙 Цена:    "+ row['Price']   +"\n" \
                        f"📦 Кол-во:  "+ str(row['Items'])
                        
                bot.send_photo(message.chat.id, row['ImgSrc'], caption=text, parse_mode="HTML", reply_markup=markup)
        if message.text == "📅 Дропы на Ethereum":
            drops = pd.read_csv(config.ETHDROPDATA ,sep='\t')
            for index, row in drops.iterrows():
                markup = types.InlineKeyboardMarkup(row_width=2)
                
                if row['TwitLink'] != '0' and row['TwitLink'] != None: 
                    markup.row(types.InlineKeyboardButton(text='Twitter', url=row['TwitLink']))

                if row['DisLink'] != '0' and row['DisLink'] != None: 
                    markup.row(types.InlineKeyboardButton(text='Discord', url=row['DisLink']))


                if row['DisLink'] != '0': 
                    disResponse = getDisResponse(row['DisLink'].split("/")[-1])
                    disOnline = str(disResponse['approximate_presence_count'])
                    disMember = str(disResponse['approximate_member_count'])
                else:
                    disOnline = 'undefiend'
                    disMember = 'undefiend'

                text =  f"📛 Имя:     "+ row['Title']   +"\n" \
                        f"📅 Дата:    "+ str(datetime.datetime.strptime(row['Date'], "%Y-%m-%dT%H:%M:%SZ"))+"\n\n" \
                        f"👥 Discord: "+ disMember      +"\n" \
                        f"🟢 Online:  "+ disOnline      +"\n\n" \
                        f"🐦 Twitter: "+ row['TwitFol'] +"\n\n" \
                        f"🪙 Цена:    "+ row['Price']   +"\n" \
                        f"📦 Кол-во:  "+ str(row['Items'])
                        
                bot.send_photo(message.chat.id, row['ImgSrc'], caption=text, parse_mode="HTML", reply_markup=markup)

bot.polling(none_stop=True)