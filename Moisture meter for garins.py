import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
import RPi.GPIO as GPIO
from time import sleep
import datetime
from firebase import firebase
import Adafruit_DHT
import datetime
import urllib2, urllib, httplib
import json
import os 
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from functools import partial



GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT11
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
# Example using a Beaglebone Black with DHT sensor
# connected to pin P8_11.
pin = 27

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


firebase = firebase.FirebaseApplication('https://raspberrypi-4fd97.firebaseio.com/', None)
#firebase.put("/dht", "/temp", "0.00")
#firebase.put("/dht", "/humidity", "0.00")

def update_firebase():
	channel = 0
	print('Reading MCP3008 values, press Ctrl-C to quit...')
	# Print nice channel column headers.
	print('| Sensor1 | Sensor2 | Sensor3 |')
	#previous statement beyatch print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
	print('-' * 57)
	# Main program loop.
    # Read all the ADC channel values in a list.
    values = [0]*3
    ss = [0]*3
    for i in range(3):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
        ss[i] = (((1023 - values[i]) / 1023) * 100)

    # Print the ADC values.
    print('| {0:>4} | {1:>4} | {2:>4} |'.format(*ss))
    #previous statement beyatch print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	now = datetime.datetime.now()
	now = str(now)
	if humidity is not None and temperature is not None:
		sleep(5)
		str_temp = ' {0:0.2f} *C '.format(temperature)	
		str_hum  = ' {0:0.2f} %'.format(humidity)
		print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))	

	
	else:
		print('Failed to get reading. Try again!')	
		sleep(10)

	data = {"temp": temperature, "humidity": humidity,"s1": ss[0],"s2": ss[1],"s3": ss[2],"now":now}
	firebase.post('/sensor/dht/', data)
	

while True:
	update_firebase()
		
        #sleepTime = int(sleepTime)
	sleep(5)
	

