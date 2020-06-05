#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from datetime import datetime
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

# logging.basicConfig(level=logging.DEBUG)

try:
    
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    # Defining fonts
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
    
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    epd.init(epd.PART_UPDATE)
    num = 0
    while (True):

        now = datetime.now()
        dateTimeInfo = now.strftime("%B %d, %H:%M")

        time_draw.rectangle((10, 10, 220, 105), fill = 255)
        time_draw.text((10, 10), dateTimeInfo, font = font15, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        if(num == 10):
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