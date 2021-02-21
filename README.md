# p8_weather.py

02/21/2021 Chris van der Meijden

A little script to get weather information from 7timer.info
and transfering the weather information to the P8 smartwatch
using uwatch2-client https://github.com/rogerdahl/uwatch2-client

To use this script you will need to set the mac address of the watch
and the latitude and longitude of your location.

If you use a special python environment, you can also set the name
of that special python executable.

This script needs to be placed in the same folder as uwatch2-client

To make this work you will need to uncomment and edit this code in 
the uwatch2lib.py:

...python
   def set_future_weather(self, args):
       arr = args.split(',')
       """Set future weather
       Args 21 bytes from C2439F
       Returns ?
       tested_and_working: False
   """
       return self._send_raw_cmd(0x42,"BBBBBBBBBBBBBBBBBBBBB",*arr)

   def set_today_weather(self, args):
       arr = args.split(',')
       """Set today weather
       Args variable length from C2439F
       Returns ?
       tested_and_working: False
   """
       return self._send_raw_cmd(0x43,"BBBBBBBBBBBBBBBBBBBBBBB",*arr)
...
