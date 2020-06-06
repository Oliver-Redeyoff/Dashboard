#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


import requests
import json
from datetime import datetime
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from io import BytesIO


try:

    # get news
    url = "https://newsapi.org/v2/top-headlines?" 
    url += "sources=bbc-news"
    url += "&apiKey=72d48922d4644d03bcda247a8ba59479"

    response = requests.get(url)
    print("got news")
    data = response.json()

    articles = []
    for article in data['articles']:
        articles.append(article['title'])


    weatherUrl = "http://api.openweathermap.org/data/2.5/weather?"
    weatherUrl += "q=Deal"
    weatherUrl += "&appid=b1fef35e73e92d824c8b42ea70b5e913"

    response = requests.get(weatherUrl)
    print("got weather")
    weatherData = response.json()
    weatherStr = "Weather in Deal : " + weatherData['weather'][0]['main']

    iconResponse = requests.get("http://openweathermap.org/img/wn/" + weatherData['weather'][0]['icon'] + ".png")
    weatherIcon = Image.open(BytesIO(iconResponse.content))
    
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    # Defining fonts
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    timeFont = ImageFont.truetype('Bellota-Regular.ttf', 22)
    weatherFont = ImageFont.truetype('OpenSans-Regular.ttf', 16)
    newsFont = ImageFont.truetype('OpenSans-Regular.ttf', 14)
    
    print("height : " + str(epd.height))
    print("width : " + str(epd.width))
    print()
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    epd.init(epd.PART_UPDATE)

    dateTimeStr = ""
    dateTimePosY = 10

    weatherPosY = 50

    newsPosY = epd.width-20
    slideX = 0
    newsIndex = 0

    num = 0

    while (True):

        # updating time section
        now = datetime.now()
        if dateTimeStr != now.strftime("%B %d, %H:%M"):
            dateTimeStr = now.strftime("%B %d, %H:%M")
            time_draw.rectangle(((0, dateTimePosY), (epd.height, dateTimePosY+timeFont.getsize(dateTimeStr)[1])), fill = 255)
            time_draw.text((10, 10), dateTimeStr, font = timeFont, fill = 0)

        # updating weather section
        time_draw.text((epd.height/2 - weatherFont.getsize(weatherStr)[0]/2, weatherPosY), weatherStr, font = weatherFont, fill = 0)
        time_draw.bitmap((250-weatherIcon.size[0], 0), weatherIcon)

        # updating news section
        time_draw.rectangle(((0, newsPosY), (epd.height, epd.width)), fill = 0)
        time_draw.text((epd.height-slideX*5, newsPosY), articles[newsIndex], font = newsFont, fill = 255)

        if (epd.height+(newsFont.getsize(articles[newsIndex])[0])-slideX*5) < 0:
            slideX = 0
            newsIndex = (newsIndex+1)%len(articles)
        slideX += 1


        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1

        if(num == 200):
            break
    
    
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd.sleep()
        
except IOError as e:
    # logging.info(e)
    print(e)
    
except KeyboardInterrupt:    
    # logging.info("ctrl + c:")
    print("exited program")
    epd2in13_V2.epdconfig.module_exit()
    exit()