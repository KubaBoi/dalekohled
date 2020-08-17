import sys
import time
import os

f =  str(sys.argv[1]) #ohniskova vzdalenost

result = time.localtime()
year = str(result.tm_year)

mon = str(result.tm_mon)
if (len(mon) == 1): mon = "0" + mon

mday = str(result.tm_mday)
if (len(mday) == 1): mday = "0" + mday

hour = str(result.tm_hour)
if (len(hour) == 1): hour = "0" + hour

min = str(result.tm_min)
if (len(min) == 1): min = "0" + min

sec = str(result.tm_sec)
if (len(sec) == 1): sec = "0" + sec

name = ("%s-%s-%s--%s-%s-%s--%smm.png" % (year, mon, mday, hour, min, sec, str(f)))

file = open("status.txt", "w")
file.write(name)
file.close()

print(name)
