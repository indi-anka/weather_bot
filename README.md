# Quick_weather_bot
Quick_weather_bot is my first pet project for getting needed weather details in fast and comfortable way.

## Description
Quick_weather_bot is a Telegram bot I've made for myself to get weather prediction info in a way appropriate for me. 
I practise riding bicycle a lot, so every time before leaving home I need to know what the temperature is, if it's going to rain and if there will be strong wind. 
These are the details the bot can show. 

## How to Use
To activate the bot user should write anything to it. In pesponse, it suggests the menu of pridictions.

There are 3 options of predictions: 'weather today', 'weather tomorrow' and 'rain today'. User chooses one of them taping a botton. 

 - 'weather today': for each hour starting from the current moment untill 11pm bot shows temperature outdoors in ... , wind speed if it's over ... and rain ammount /
 common description of the weather, like 'sunny'/'cloudy'/etc.
 
 - 'weather tomorrow': the same info for each hour from 9am to 23pm for the next day
 
 - 'rain today': 

## About the project
The bot is written in Python with usage of PyTelegramBotAPI (Telebot). 

For the predictions it uses API from https://openweathermap.org.

The time zone is set authomatically. The geographical position is defined as StPetersburg, Russia. To expand the bot's applicability, I plan to add the choice of geoposition.
