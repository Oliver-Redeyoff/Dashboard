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
import sched
from PIL import Image,ImageDraw,ImageFont
import traceback
from io import BytesIO


articles = []
weatherIcon = None
greetingStr = ""
syncFrequency = 10
s = sched.scheduler(time.time, time.sleep)


def sync():
    global articles, weatherIcon, greetingStr, syncFrequency, s

    print("syncing data")
    articles = getNews()
    weatherIcon = getWeather()

    hour = int(datetime.now().hour)
    if hour >= 3 and hour < 12:
        greetingStr = "Good morning Oliver :)"
    elif hour >= 12 and hour < 6:
        greetingStr = "Good afternoon Oliver :)"
    elif hour >= 6 and hour < 3:
        greetingStr = "Good evening Oliver :)"
    else :
        greetingStr = "Hello there Oliver :)"

    s.enter(syncFrequency, 1, sync)

def getNews():
    url = "https://newsapi.org/v2/top-headlines?" 
    url += "sources=bbc-news"
    url += "&apiKey=72d48922d4644d03bcda247a8ba59479"

    response = requests.get(url)
    print("got news")
    data = response.json()

    articles = []
    for article in data['articles']:
        articles.append(article['title'])
    
    return articles

def getWeather():
    weatherUrl = "http://api.openweathermap.org/data/2.5/weather?"
    weatherUrl += "q=Deal"
    weatherUrl += "&appid=b1fef35e73e92d824c8b42ea70b5e913"

    response = requests.get(weatherUrl)
    print("got weather")
    weatherData = response.json()
    # weatherStr = "Weather in Deal : " + weatherData['weather'][0]['main']

    iconResponse = requests.get("http://openweathermap.org/img/wn/" + weatherData['weather'][0]['icon'] + ".png")
    weatherIcon = Image.open(BytesIO(iconResponse.content))

    return weatherIcon


try:

    # get new weather and news data
    sync()
    
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    # Defining fonts
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    timeFont = ImageFont.truetype('Bellota-Regular.ttf', 22)
    greetingFont = ImageFont.truetype('OpenSans-Regular.ttf', 22)
    newsFont = ImageFont.truetype('OpenSans-Regular.ttf', 14)
    
    # this is the image that will be display on the e-display
    dash_image = Image.new('1', (epd.height, epd.width), 255)
    dash_draw = ImageDraw.Draw(dash_image)
    
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(dash_image))
    
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
            dash_draw.rectangle(((0, dateTimePosY), (epd.height, dateTimePosY+timeFont.getsize(dateTimeStr)[1])), fill = 255)
            dash_draw.text((10, 10), dateTimeStr, font = timeFont, fill = 0)

        # updating weather section
        dash_draw.bitmap((250-weatherIcon.size[0], 0), weatherIcon)

        # updating greeting section
        dash_draw.text((epd.height/2-greetingFont.getsize(greetingStr)[0]/2, 50), greetingStr, font = greetingFont, fill = 0)

        # updating news section
        dash_draw.rectangle(((0, newsPosY), (epd.height, epd.width)), fill = 0)
        dash_draw.text((epd.height-slideX*5, newsPosY), articles[newsIndex], font = newsFont, fill = 255)

        if (epd.height+(newsFont.getsize(articles[newsIndex])[0])-slideX*5) < 0:
            slideX = 0
            newsIndex = (newsIndex+1)%len(articles)
        slideX += 1


        epd.displayPartial(epd.getbuffer(dash_image))
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