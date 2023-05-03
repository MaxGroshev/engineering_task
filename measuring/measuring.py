import sys
import time
import matplotlib.pyplot as plt
import RPi.GPIO as gpio
gpio.setmode (gpio.BCM)

dac  = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

gpio.setmode (gpio.BCM)
gpio.setup   (dac, gpio.OUT)
gpio.setup   (leds, gpio.OUT)
gpio.setup   (troyka, gpio.OUT, initial = 1)
gpio.setup   (comp, gpio.IN)

def adc ():
    val = 0
    for i in range (7, -1, -1):
        val += 2**i
        gpio.output (dac, dec_to_bin (val))
        time.sleep (0.001)
        if gpio.input (comp) == 0:
            val -= 2**i
    return val

def dec_to_bin (i):
    return [int (elem) for elem in bin (i) [2:].zfill (8)]    

try:
    value = 0
    meas_res = []
    num = 0
    start_time = time.time()

    while (num < 500):
        value = adc ()
        meas_res.append (value)
        gpio.output(leds, dec_to_bin (value))
        num += 1
    
    gpio.output (troyka, 0)

    while (num < 1000):
        value = adc ()
        meas_res.append (value)
        gpio.output(leds, dec_to_bin (value))
        num += 1

    end_time = time.time ()
    delta = (end_time - start_time) / num
    measured_data_str = [str (item) for item in meas_res]
    with open ("data.txt", "w") as outfile:
        outfile.write ("\n".join (measured_data_str))

    # y = [i/256*3.3 for i in meas_res]
    # x = [i * delta for i in range (len (meas_res))]
    plt.plot (meas_res)
    plt.show ()


finally:
    gpio.output  (leds, 0)
    gpio.output  (dac,  0)
    gpio.cleanup ()