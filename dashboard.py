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


try:

    # get news
    url = "https://newsapi.org/v2/top-headlines?" 
    url += "sources=bbc-news"
    url += "&apiKey=72d48922d4644d03bcda247a8ba59479"

    articles = []

    response = requests.get(url)
    print("got news")
    data = response.json()

    for article in data['articles']:
        articles.append(article['title'])
    
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    # Defining fonts
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    timeFont = ImageFont.truetype('Bellota-Regular.ttf', 22)
    newsFont = ImageFont.truetype('OpenSans-Regular.ttf', 14)
    
    print("height : " + str(epd.height))
    print("width : " + str(epd.width))
    print()
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    epd.init(epd.PART_UPDATE)
    num = 0
    while (True):

        now = datetime.now()
        dateTimeInfo = now.strftime("%B %d, %H:%M")

        time_draw.rectangle(((0, 10), (epd.height, 70)), fill = 255)
        time_draw.text((10, 10), dateTimeInfo, font = timeFont, fill = 0)
        time_draw.text((10-num*4, 50), articles[0], font = newsFont, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1

        # time.sleep(2)

        if(num == 50):
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