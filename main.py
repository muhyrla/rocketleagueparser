from typing import List, Any

import requests
from bs4 import BeautifulSoup
from search_item_id import searchitemid
from search_color_id import searchcolorid
from search_itemwithcategory_id import searchitemid_withcategory
from urllib.parse import urlencode
import telebot

key = '5762344619:AAFu_ADKKaEHbNxXTvaIwJqDzagrjmlCGuQ'
bot = telebot.TeleBot(key)
CATEGORIES = {"Wheels", "Antennas", "Banners", "Bodies", "Decals", "Audio", "Goal", "Misc", "Paint", "Boosts", "Toppers", "Trails", "Wheels"}


def gettrade(tdata):
    items_div = tdata.find('div', {'class': 'rlg-trade__items'})

    div_has = items_div.find('div', {'class': 'rlg-trade__itemshas'})
    items_has = div_has.find_all('div', {'class': 'rlg-item'})

    div_wants = items_div.find('div', {'class': 'rlg-trade__itemswants'})
    items_want = div_wants.find_all('div', {'class': 'rlg-item'})

    username = tdata.find('a', {'class': 'rlg-trade__user'})
    userlink = username.get('href')
    username = userlink.split("/")[-1].replace("\n", "")

    time = tdata.find('span', {'class': 'rlg-trade__time'}).text.split("\n")[1]

    rank = tdata.find('span', {'class': 'rlg-rank'})
    if rank:
        rank = rank.text.replace("\n", "")
    return items_has, items_want, username, time, rank


def create_answer(trs, item_name, cr):
    preanswer = []
    for trade in trs:
        h, w, user, t, r = gettrade(trade) # Получить имеющиеся, хочеющиеся, юзера ранг и время
        for i in range(0, len(h)):
            if len(h) != len(w):
                break

            item_name_has = h[i].find('div', {'class': 'rlg-item__text'}).text.replace("\n", "")
            item_name_wants = w[i].find('div', {'class': 'rlg-item__text'}).text.replace("\n", "")
            try:
                item_color_has = h[i].find('div', {'class': 'rlg-item__paint'}).text.replace('\n', '').replace(' ', '')
            except AttributeError:
                item_color_has = 'None'
            try:
                item_color_wants = h[i].find('div', {'class': 'rlg-item__paint'}).text.replace('\n', '').replace(' ', '')
            except AttributeError:
                item_color_wants = 'None'
            if item_name_has == item_name or item_name_wants == item_name:
                if (cr == 'Any') or (cr == item_color_wants):
                    print(cr, item_color_has, item_color_wants)
                    try:
                        item_quant_has = h[i].find('div', {'class': 'rlg-item__quantity'}).text.replace("\n",  "")
                    except AttributeError:
                        item_quant_has = 1
                    try:
                        item_quant_wants = w[i].find('div', {'class': 'rlg-item__quantity'}).text.replace("\n",  "")
                    except AttributeError:
                        item_quant_wants = 1
                    preanswer.append([item_name_has, str(item_quant_has), item_name_wants, str(item_quant_wants), user, r, t])
    return preanswer


@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.chat.type == 'private':
        item, color, category = message.text.split(":")
        if category == 'Any':
            if searchcolorid(color) and searchitemid(item):
                item_id = searchitemid(item)
                if color == 'None':
                    color_id = 'N'
                else:
                    color_id = searchcolorid(color)
                query_params = {
                    "filterItem": item_id,
                    "filterCertification": "0",
                    "filterPaint": color_id,
                    "filterTradeType": "0",
                    "filterMinCredits": "0",
                    "filterMaxCredits": "100000",
                    "filterSearchType": "1",
                    "filterItemType": "0"
                }
                url_forsale = f"https://rocket-league.com/trading?{urlencode(query_params)}&filterPlatform%5B%5D=1"
                query_params = {
                    "filterItem": item_id,
                    "filterCertification": "0",
                    "filterPaint": color_id,
                    "filterTradeType": "0",
                    "filterMinCredits": "0",
                    "filterMaxCredits": "100000",
                    "filterSearchType": "2",
                    "filterItemType": "0"
                }
                url_tobuy = f"https://rocket-league.com/trading?{urlencode(query_params)}&filterPlatform%5B%5D=1"
            else:
                bot.send_message(message.chat.id, "Предмет не найден, попробуйте исправить запрос и повторить.")
                url_forsale = None
                url_tobuy = None
        elif category in CATEGORIES:
            category = category.lower()
            if searchcolorid(color) and searchitemid_withcategory(item, category):
                item_id = searchitemid_withcategory(item, category)
                if color == 'None':
                    color_id = 'N'
                else:
                    color_id = searchcolorid(color)
                query_params = {
                    "filterItem": item_id,
                    "filterCertification": "0",
                    "filterPaint": color_id,
                    "filterTradeType": "0",
                    "filterMinCredits": "0",
                    "filterMaxCredits": "100000",
                    "filterSearchType": "1",
                    "filterItemType": "0"
                }
                url_forsale = f"https://rocket-league.com/trading?{urlencode(query_params)}&filterPlatform%5B%5D=1"
                query_params = {
                    "filterItem": item_id,
                    "filterCertification": "0",
                    "filterPaint": color_id,
                    "filterTradeType": "0",
                    "filterMinCredits": "0",
                    "filterMaxCredits": "100000",
                    "filterSearchType": "2",
                    "filterItemType": "0"
                }
                url_tobuy = f"https://rocket-league.com/trading?{urlencode(query_params)}&filterPlatform%5B%5D=1"
            else:
                bot.send_message(message.chat.id, "Предмет не найден, попробуйте исправить запрос и повторить.")
                url_forsale = None
                url_tobuy = None
        else:
            bot.send_message(message.chat.id, "Предмет не найден, попробуйте исправить запрос и повторить.")
            url_forsale = None
            url_tobuy = None

        print(message.text, '\n', url_forsale, '\n', url_tobuy)
        if url_forsale != None:
            data = requests.get(url_forsale)
            soup = BeautifulSoup(data.text, 'html.parser')
            trades = soup.find_all('div', {'class': 'rlg-trade'})
            ans = create_answer(trades, item, color)
            r_s = sorted(ans, key=lambda x: x[3], reverse=False)
            reply = ''
            for i in range(0, len(r_s)):
                reply = f"{reply}{r_s[i][0]}:{r_s[i][1]} = {r_s[i][2]}:{r_s[i][3]} | ({r_s[i][5]}){r_s[i][4]} | {r_s[i][6]}\n"
            bot.send_message(message.chat.id, f"Предложения на продажу:\n{reply[:4069]}")

        if url_tobuy != None:
            data = requests.get(url_tobuy)
            soup = BeautifulSoup(data.text, 'html.parser')
            trades = soup.find_all('div', {'class': 'rlg-trade'})
            ans = create_answer(trades, item, color)
            r_s = sorted(ans, key=lambda x: x[1], reverse=True)
            reply = ''
            for i in range(0, len(r_s)):
                reply = f"{reply}{r_s[i][0]}:{r_s[i][1]} = {r_s[i][2]}:{r_s[i][3]} | ({r_s[i][5]}){r_s[i][4]} | {r_s[i][6]}\n"
            bot.send_message(message.chat.id, f"Предложения на покупку:\n{reply[:4069]}")

bot.polling()