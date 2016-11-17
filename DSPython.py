#!/usr/bin/env python
#
# ______                                  _    _              ______              _         ______ _           
#(_____ \                                | |  | |            (______)            | |       / _____) |          
# _____) )__  _ _ _ _____  ____ _____  __| |  | |__  _   _    _     _ _____  ____| |  _   ( (____ | |  _ _   _ 
#|  ____/ _ \| | | | ___ |/ ___) ___ |/ _  |  |  _ \| | | |  | |   | (____ |/ ___) |_/ )   \____ \| |_/ ) | | |
#| |   | |_| | | | | ____| |   | ____( (_| |  | |_) ) |_| |  | |__/ // ___ | |   |  _ (    _____) )  _ (| |_| |
#|_|    \___/ \___/|_____)_|   |_____)\____|  |____/ \__  |  |_____/ \_____|_|   |_| \_)  (______/|_| \_)\__  |
#                                                   (____/                                              (____/ 
# A python program which uses publically available
# web apis to find out what the weather is.
#
 
# You'll need an API key below... you can get 1000 requests per day for free.
# Go to https://darksky.net/dev/ and sign up.
 
API="PUT_YOUR_OWN_API_KEY_HERE"
URL="https://api.darksky.net/forecast/"
 
# Change the below for your latitude and longitude, Below figures are for the centre of Brussels, Belgium.
LAT= 50.8467
LNG= 4.3526

# Change the below for different measurement units, values are :
# auto = automatically select based upon geographical region
# ca = same as si, except windSpeed is in kilometers per hour
# uk2 = same as si, except that nearestStormDistance and visibility are in miles and windSpeed is in miles per hour
# us = Imperial units
# si : SI units 
UTS="si"

directions = ["N", "NNE", "ENE", "E", "ESE", "SSE", "S", "SSW", "WSW", "W", "WNW", "NNW"]
 
def bearing_to_direction(bearing):
    d = 360. / 12.
    return directions[int((bearing+d/2)/d)]
     
import sys
import os
import time
import optparse
import json
 
import urllib2
 
now = time.time()
cached = False
 
if os.path.exists("WEATHER.cache"):
    f = open("WEATHER.cache")
    parsed = json.loads(f.read())
    f.close()
    if now - parsed["currently"]["time"] < 900:
        cached = True
 
if cached:
    print "::: Using cached data..."
else:
    print "::: Reloading cache..."
    req = urllib2.Request(URL+API+"/"+("%f,%f"%(LAT,LNG)+"?units="+UTS))
    response = urllib2.urlopen(req)
    parsed = json.loads(response.read())
    f = open("WEATHER.cache", "w")
    f.write(json.dumps(parsed, indent=4, sort_keys=True))
    f.close() ;
 
c = parsed["currently"]
print ":::", time.strftime("%F %T", time.localtime(c["time"]))
print "::: Conditions:", c["summary"]
print "::: Temperature:", ("%.1f" % c["temperature"])+u"\u00B0"
print "::: Feels Like:", ("%.1f" % c["apparentTemperature"])+u"\u00B0"
print "::: Dew Point:", ("%.1f" % c["dewPoint"])+u"\u00B0"
print "::: Humidity:", ("%4.1f%%" % (c["humidity"]*100.))
print "::: Wind:", int(round(c["windSpeed"])), "mph", bearing_to_direction(c["windBearing"])
 
d = parsed["daily"]["data"][0]
print "::: High:", ("%.1f" % d["temperatureMax"])+u"\u00B0"
print "::: Low:", ("%.1f" % d["temperatureMin"])+u"\u00B0"
 
d = parsed["hourly"]["data"]
 
for x in d[:12]:
        print time.strftime("\t%H:%M", time.localtime(x["time"])), x["summary"], ("%.1f" % x["temperature"])+u"\u00B0"
