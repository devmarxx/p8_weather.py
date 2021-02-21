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

```python
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
```

Byte description:

Today (First Byte D0):

(0x43,"BBBBBBBBBBBBBBBBBBBBBBB",0,0,4,0,32,0,32,0,32,0,32,0,110,0,117,0,108,0,108,0,77,0,6)

Future (First Byte D0):

(0x42,"BBBBBBBBBBBBBBBBBBBBB",0,1,8,0,0,6,0,253,5,0,255,6,3,2,10,3,5,11,0,4,11)

Home screen:

* Temperature range Future D1-D2
* Icon Today D1

Weather screen:

* Temperature Today D2
* Icon Today D1
* Temperature range Future D1-D2
* Tomorrow Future D4-D5

Week screen (DAYS after tomorrow):

* DAY1 temperature range Future D7-D8 Icon Future D6
* DAY2 temperature range Future D10-D11 Icon Future D9
* DAY3 temperature range Future D13-D14 Icon Future D12
* DAY4 temperature range Future D15-D16 Icon Future D14

Temperatures: 255 is -1, 254 is -2, ...

Icons:

* 0 Cloud with sun
* 1 Fog
* 2 Cloud
* 3 Cloud with heavy rain
* 4 Cloud with rain
* 5 Sun

Console output:

```bash command-line
---------------------------------
Todays temperature: 3
Weather: pcloudy
Range: 3 - 10
---------------------------------
Tomorrow range: 0 - 10
---------------------------------
TUE
Weather: clear
Range: 1 - 11
---------------------------------
WED
Weather: clear
Range: 1 - 11
---------------------------------
THU
Weather: clear
Range: 2 - 12
---------------------------------
FRI
Weather: cloudy
Range: 3 - 11
---------------------------------

INFO     Starting...
INFO     Using MAC address provided by client: xx:xx:xx:xx:xx:xx
INFO     Connecting to MAC xx:xx:xx:xx:xx:xx...
INFO     ok
INFO     Starting...
INFO     Using MAC address provided by client: xx:xx:xx:xx:xx:xx
INFO     Connecting to MAC xx:xx:xx:xx:xx:xx...
INFO     ok

---------------------------------
Done
```
