import telebot
from telebot import types
import time
import requests
from tokens import TG_TOKEN, OW_URL_TOKEN


def split_marker(marker):
    day = 'today' if 'today' in marker else 'tomorrow'
    need_rain = 'rain' in marker
    return day, need_rain


def calc_start_stop_index(hours, day):
    unix_timestamp = int(hours[0]['dt'])
    datetime_struct = time.localtime(unix_timestamp)
    hour = int(time.strftime('%H', datetime_struct))
    start_hour = 9
    if day == 'today':
        if hour < 9:
            start = 9 - hour
        else:
            start = 0
            start_hour = hour
        stop = 24 - hour
    else:
        start = 33 - hour
        stop = start + 15
    return start, start_hour, stop
    

def get_weather(hours, day):
    start, hour, stop = calc_start_stop_index(hours, day)
    answer = ''
    for i in range(start, stop):
        temp = str(int(hours[i]['temp']))
        wind = int(hours[i]['wind_speed'])
        wind_for_user = ' ветер-' + str(wind) if wind >= 8 else ''
        main = hours[i]['weather']
        weather = main[0]['description']
        rain_amount = hours[i]['rain']['1h'] if 'rain' in hours[i] else ''
        answer += f'{hour}:00\nt={temp} {wind_for_user} {weather} {rain_amount}\n'
        hour += 1
    return answer
    

def get_rain(hours, day):
    start, hour, stop = calc_start_stop_index(hours, day)
    answer = ''
    for i in range(start, stop):
        rain_amount = hours[i]['rain']['1h'] if 'rain' in hours[i] else '0'
        answer += f'{hour}:00 - {rain_amount}\n'
        hour += 1
    return answer


def prediction(hours, marker):
    day, need_rain = split_marker(marker)
    answer = 'дождь' if need_rain else 'погода'
    answer += ' '
    answer += 'сегодня' if day == 'today' else 'завтра'
    answer += '\n'
    if need_rain:
        answer += get_rain(hours, day)
    else:
        answer += get_weather(hours, day)
    return answer


def ask_api(marker):
    URL = OW_URL_TOKEN
    r = requests.get(url=URL)
    response = r.json()
    hours = response['hourly']
    return prediction(hours, marker)


bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text_meanings = []
    text_meanings.append(['Погода сегодня', 'weather_today'])
    text_meanings.append(['Погода завтра', 'weather_tomorrow'])
    text_meanings.append(['Дождь', 'rain_today'])
    keyboard = types.InlineKeyboardMarkup()
    for text_meaning in text_meanings:
        key = types.InlineKeyboardButton(text=text_meaning[0], callback_data=text_meaning[1])
        keyboard.add(key)
    if message.text:
        bot.send_message(message.from_user.id, 'Выберите опцию', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Чтобы узнать погоду, напишите то-нибудь')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
        msg = ask_api(call.data)
        bot.send_message(call.message.chat.id, msg)


bot.polling(none_stop=True, interval=0)
