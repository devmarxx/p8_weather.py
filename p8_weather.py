# p8_weather.py
#
# 02/21/2021 Chris van der Meijden
#
# A little script to get weather information from 7timer.info
# and transfering the weather information to the P8 smartwatch
# using uwatch2-client https://github.com/rogerdahl/uwatch2-client
#
# To use this script you will need to set the mac address of the watch
# and the latitude and longitude of your location.
#
# If you use a special python environment, you can also set the name
# of that special python executable.
#
# This script needs to be placed in the same folder as uwatch2-client
#
# To make this work you will need to uncomment and edit this code in 
# the uwatch2lib.py:
#
#     def set_future_weather(self, args):
#        arr = args.split(',')
#        """Set future weather
#        Args 21 bytes from C2439F
#        Returns ?
#        tested_and_working: False
#    """
#        return self._send_raw_cmd(0x42,"BBBBBBBBBBBBBBBBBBBBB",*arr)
#
#    def set_today_weather(self, args):
#        arr = args.split(',')
#        """Set today weather
#        Args variable length from C2439F
#        Returns ?
#        tested_and_working: False
#    """
#        return self._send_raw_cmd(0x43,"BBBBBBBBBBBBBBBBBBBBBBB",*arr)
#
#

import requests
import xml.etree.ElementTree as ET

import os
import datetime
from datetime import timedelta

weekDays = ("MON","TUE","WED","THU","FRI","SAT","SUN")
# It is not understood by now, why we need to substract 15 hours to get a 
# "near actual time" temperature. How does this behave on different longitudes?
hourNow = (datetime.datetime.now() - timedelta(hours=15)).hour

# Put your python version here if needed (i.e. python3.9)
my_env = ""

# Put mac of your watch here
mac = "xx:xx:xx:xx:xx:xx"

# Put your location here
lat = 48.85
lon = 2.29

tc = 0
stc = 0
dc = 0
future = "0,"
today = "0,"
icon = "0"
tempnow = "0"
nearest = "0"

if hourNow < 24:
   stc = 8
if hourNow < 21:
   stc = 7
if hourNow < 18:
   stc = 6
if hourNow < 15:
   stc = 5
if hourNow < 12:
   stc = 4
if hourNow < 9:
   stc = 3
if hourNow < 6:
   stc = 2
if hourNow < 3:
   stc = 1

# converter for negative temperatures
def conv_negative(temp):
    my_temp = int(temp)
    if my_temp < 0:
       my_temp = 256 + my_temp
    my_temp = str(my_temp)
    return my_temp

# get nearest temperature
url = 'http://www.7timer.info/bin/civil.php?lon={}&lat={}ac=0&unit=metric&output=xml&tzshift=0'.format(lon,lat)

r = requests.get(url)

root = ET.fromstring(r.content)

for node in root.iter():
    # catch the nearest temp2m
    if node.tag == "temp2m":
       tc = tc + 1
       nearest = conv_negative(node.text)
       if tc == stc:
          temp_now = nearest

nearest = temp_now

# define the icons
def set_icon(val):
    my_icon = "3"
    if val == "clear":
       my_icon = "5"
    if val == "pcloudy":
       my_icon = "0"
    if val == "mcloudy":
       my_icon = "0"
    if val == "cloudy":
       my_icon = "0"
    if val == "vcloudy":
       my_icon = "2"
    if val == "foggy":
       my_icon = "1"
    if val == "lrain":
       my_icon = "4"
    return my_icon

# Now lets get the rest of the data
url = 'http://www.7timer.info/bin/civillight.php?lon={}&lat={}ac=0&unit=metric&output=xml&tzshift=0'.format(lon,lat)

r = requests.get(url)

root = ET.fromstring(r.content)

for node in root.iter():
    # catch only the data we need
    if node.tag == "weather":
       dc = dc + 1
    # build today and tomorrow
    if dc == 1 and node.tag == "weather":
      # set todays icon
      today = today + set_icon(node.text) + "," + nearest + ",0,32,0,32,0,32,0,32,0,110,0,117,0,108,0,108,0,77,0,6"
      ostr1 = "Todays temperature: " + nearest
      ostr2 = "Weather: " + node.text
      print ("")
      print ("---------------------------------")
      print (ostr1)
      print (ostr2)
    # set min and max for today
    if dc == 1 and node.tag == "temp2m_max":
      temp2m_max = conv_negative(node.text)
      ht2_max = node.text
    if dc == 1 and node.tag == "temp2m_min":
      temp2m_min = conv_negative(node.text)
      future = future + temp2m_min + "," + temp2m_max + ",0,"
      ostr3 = "Range: " + node.text + " - " + ht2_max
      print (ostr3)
      print ("---------------------------------")

    # set min and max for tomorrow
    if dc == 2 and node.tag == "temp2m_max":
      temp2m_max = conv_negative(node.text)
      ht2_max = node.text
    if dc == 2 and node.tag == "temp2m_min":
      temp2m_min = conv_negative(node.text)
      future = future + temp2m_min + "," + temp2m_max + ","
      ostr4 = "Tomorrow range: " + node.text + " - " + ht2_max
      print (ostr4)
      print ("---------------------------------")

    # set DAY1 after tomorrow
    if dc == 3 and node.tag == "weather":
      # set icon
      future = future + set_icon(node.text) + ","
      daynr = datetime.datetime.today().weekday() + 2
      if daynr > 6:
         daynr = daynr - 7
      DAY = weekDays[daynr]
      print (DAY)
      ostr5 = "Weather: " + node.text
      print (ostr5)
    if dc == 3 and node.tag == "temp2m_max":
      temp2m_max = conv_negative(node.text)
      ht2_max = node.text
    if dc == 3 and node.tag == "temp2m_min":
      temp2m_min = conv_negative(node.text)
      future = future + temp2m_min + "," + temp2m_max + ","
      ostr6 = "Range: " + node.text + " - " + ht2_max
      print (ostr6)
      print ("---------------------------------")

    # set DAY2 after tomorrow
    if dc == 4 and node.tag == "weather":
      # set icon
      future = future + set_icon(node.text) + ","
      daynr = datetime.datetime.today().weekday() + 3
      if daynr > 6:
         daynr = daynr - 7
      DAY = weekDays[daynr]
      print (DAY)
      ostr5 = "Weather: " + node.text
      print (ostr5)
    if dc == 4 and node.tag == "temp2m_max":
      temp2m_max = conv_negative(node.text)
      ht2_max = node.text
    if dc == 4 and node.tag == "temp2m_min":
      temp2m_min = conv_negative(node.text)
      future = future + temp2m_min + "," + temp2m_max + ","
      ostr6 = "Range: " + node.text + " - " + ht2_max
      print (ostr6)
      print ("---------------------------------")

    # set DAY3 after tomorrow
    if dc == 5 and node.tag == "weather":
      # set icon
      future = future + set_icon(node.text) + ","
      daynr = datetime.datetime.today().weekday() + 4
      if daynr > 6:
         daynr = daynr - 7
      DAY = weekDays[daynr]
      print (DAY)
      ostr5 = "Weather: " + node.text
      print (ostr5)
    if dc == 5 and node.tag == "temp2m_max":
      temp2m_max = conv_negative(node.text)
      ht2_max = node.text
    if dc == 5 and node.tag == "temp2m_min":
      temp2m_min = conv_negative(node.text)
      future = future + temp2m_min + "," + temp2m_max + ","
      ostr6 = "Range: " + node.text + " - " + ht2_max
      print (ostr6)
      print ("---------------------------------")

    # set DAY4 after tomorrow
    if dc == 6 and node.tag == "weather":
      # set icon
      future = future + set_icon(node.text) + ","
      daynr = datetime.datetime.today().weekday() + 5
      if daynr > 6:
         daynr = daynr - 7
      DAY = weekDays[daynr]
      print (DAY)
      ostr5 = "Weather: " + node.text
      print (ostr5)
    if dc == 6 and node.tag == "temp2m_max":
      temp2m_max = conv_negative(node.text)
      ht2_max = node.text
    if dc == 6 and node.tag == "temp2m_min":
      temp2m_min = conv_negative(node.text)
      future = future + temp2m_min + "," + temp2m_max + ",0,4,11"
      ostr6 = "Range: " + node.text + " - " + ht2_max
      print (ostr6)
      print ("---------------------------------")
      print ("")

my_cmd = my_env + " ./uwatch2-client.py --mac " + mac + " "
my_cmd = my_cmd + "'set-future-weather " + future + "'"
os.system(my_cmd)

my_cmd = my_env + " ./uwatch2-client.py --mac " + mac + " "
my_cmd = my_cmd + "'set-today-weather " + today + "'"
os.system(my_cmd)

print ("")
print ("---------------------------------")
print ("Done")
print ("")
