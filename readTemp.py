import os
import time
import datetime
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

if not os.path.exists( "/sys/devices/platform/bone_capemgr/slots" ):
    os.system( 'echo \'BB-W1-P9.12\' > /sys/devices/platform/bone_capemgr/slots' )

temp_sensor = '/sys/bus/w1/devices/28-0000075d0c03/w1_slave'

def temp_raw():

	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	
	lines = temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = temp_raw()
	
	temp_output = lines[1].find('t=')

	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	return st + " " + str(temp_c)

while True:
    publish.single( "beaglebone/corys_hive_1/temp", read_temp(), hostname="beeconnections.com", protocol=mqtt.MQTTv31 )
    
    time.sleep(300)
