import time
import RPi.GPIO as gpio
import sys
dac = [26, 19, 13, 6, 5, 11, 9, 10]

gpio.setmode (gpio.BCM)
gpio.setup   (dac, gpio.OUT)

def dec_to_bin (i, n):
    return [int (elem) for elem in bin (i) [2:].zfill (n)]
try:
    period = int (input ('input time of sleeping'))
    while (True):
        for i in range (0, 256):
            gpio.output (dac, dec_to_bin (int (i), 8))
            print ("{:.4f}".format (int (i)/256*3.3))
            time.sleep (period)

except ValueError:
    print ('NuMbEr')
except KeyboardInterrupt:
    print ('Ok')

finally:
    gpio.output  (dac, 0)
    gpio.cleanup ()