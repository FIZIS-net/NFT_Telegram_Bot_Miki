from pydoc import describe
import telebot
import config
import requests
import datetime
from datetime import date
from datetime import timedelta
import time
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

def createDropMessageContent(drop):
    markup = types.InlineKeyboardMarkup(row_width=2)
    disMember = "❌"
    disOnline = "❌"
    if drop['twitter'] != None:
        try:
            markup.add(types.InlineKeyboardButton(text='Twitter', url=drop['twitter']))
        except:
            markup.add(types.InlineKeyboardButton(text='Twitter ❌'))
    if drop['discord'] != None:
        try:
            markup.add(types.InlineKeyboardButton(text='Discord', url=drop['discord']))
        except:
            markup.add(types.InlineKeyboardButton(text='Discord ❌'))
    if drop['discord'] != None: 
        disResponse = getDisResponse(str(drop['discord']).split("/")[-1])
        if disResponse['code'] != 10006:
            try:
                disOnline = str(disResponse['approximate_presence_count'])
            except:
                print(disResponse)
            try:
                disMember = str(disResponse['approximate_member_count'])
            except:
                print(disResponse)
        else:
            disOnline = '❌'
            disMember = '❌'
    if drop['website']:
        website = drop['website']
    else:
        website = '❌'

    text =  f"📛 Имя:     "+ drop['name']   +"\n" \
            f"📅 Дата:    "+ drop['date']      +"\n\n" \
            f"👥 Discord: "+ disMember      +"\n" \
            f"🟢 Online:  "+ disOnline      +"\n\n" \
            f"🌐 Сайт:  "+ website      + "\n" \
            f"🪙 Цена:    "+ drop['price']  +"\n" \
            f"📦 Кол-во:  "+ str(drop['nft_count'])

    
    return {'textMessage': text,'markup': markup}

def createMagicDropMessageContent(drop):
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        if(drop['launchDate']):
            dropDate =  datetime.datetime.strptime(drop['launchDate'], "%Y-%m-%dT%H:%M:%S.%f%z") + timedelta(hours=3)
        else:
            dropDate = "❌"
        dropDate = dropDate.strftime("%d/%m/%Y %H:%M")
        text =  f"📛 Имя:     " + drop['name'] +"\n" \
                f"📅 Дата:    " + dropDate +"\n\n" \
                f"🪙 Цена:    " + str(drop['price']) +"\n" \
                f"📦 Кол-во:  " + str(drop['size']) +"\n" \
                f"📄 Описание:    " + drop['description']

        return {'textMessage': text,'markup': markup}
    except:
        print(drop)
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📈 Курс SOL","📈 Курс ETH")
    markup.row("🗓️ Дропы Solana на сегодня")
    markup.row("📅 Все дропы Solana")
    markup.row("✨ MagicEden дропы на сегодня")

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n Я - {1.first_name}, твой личный помощник в мире NFT".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handler(message):
    if message.chat.type == 'private':
        match message.text:
            case "📈 Курс SOL":
                bot.send_message(message.chat.id, "SOL= " + str(reqRate('sol'))+"$")
            case "📈 Курс ETH":
                bot.send_message(message.chat.id, "ETH= " + str(reqRate('eth'))+"$")
            case "🗓️ Дропы Solana на сегодня":
                with open('solDrop.json') as file:
                    drops = json.load(file)
                    drops = drops['result']['data'][str(date.today())]
                for drop in drops:
                    messageContent = createDropMessageContent(drop)
                    try:
                        bot.send_photo(message.chat.id, drop['image'], caption= messageContent['textMessage'], parse_mode="HTML", reply_markup=messageContent['markup'])
                        time.sleep(0.5)
                    except Exception as e:
                        print(e)
                        print(drop)

            case "📅 Все дропы Solana":
                with open('solDrop.json') as file:
                    drops = json.load(file)
                    drops = drops['result']['data'][str(date.today())]
                for drop in drops:
                    messageContent = createDropMessageContent(drop)
                    bot.send_photo(message.chat.id, drop['image'], caption= messageContent['textMessage'], parse_mode="HTML", reply_markup=messageContent['markup'])
                    time.sleep(0.5)
            case "✨ MagicEden дропы на сегодня":
                with open('magicDrop.json') as file:
                    drops = json.load(file)
                for drop in drops:
                    messageContent = createMagicDropMessageContent(drop)
                    try:
                        bot.send_photo(message.chat.id, drop['image'], caption= messageContent['textMessage'], parse_mode="HTML", reply_markup=messageContent['markup'])
                    except Exception as e:
                        print(e)
                        print(drop)

                    time.sleep(0.5)
                


bot.polling(none_stop=True)