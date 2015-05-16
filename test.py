import RPi.GPIO as gpio
import time

#INITIAL SETUP
enable_pin=10 #Marked MOSI on the paddle board
left_forward=5
left_reverse=6
right_forward=20
right_reverse=16

def gpio_init():
	gpio.cleanup() #clear all settings
	gpio.setmode(gpio.BCM) #use the Broadcom numbering scheme
	gpio.setup(enable_pin, gpio.OUT) #the enable pin that turns on the motor
	gpio.output(enable_pin, gpio.LOW) #now set it low to make sure it's not on
	
	## set the four wheels
	gpio.setup(left_forward, gpio.OUT)
	gpio.setup(left_reverse, gpio.OUT)
	gpio.setup(right_forward, gpio.OUT)
	gpio.setup(right_reverse, gpio.OUT)
	
def gpio_reset_all():
	#set all GPIOs to low
	gpio.output(left_forward, gpio.LOW)
	gpio.output(left_reverse,gpio.LOW)
	gpio.output(right_forward, gpio.LOW)
	gpio.output(right_reverse,gpio.LOW)
	
def go(direction, duration,gear):
	
	gear=int(gear)
	gpio_reset_all()
	
	#the number here represents a percentage of the total available speed
	if gear==1:
		speed=65
	elif gear==2:
		speed=70
	elif gear==3:
		speed=75
	elif gear==4:
		speed=80
	elif gear==5:
		speed=95
	else:
		speed=100
	
	print speed
		
	pwm=gpio.PWM(enable_pin, 50)#50 is the frequency
	pwm.start(speed) #a "speed" of 50, sends power exactly every second cycle
	
	if direction=="forward":
		print "forward"
		gpio.output(right_forward, gpio.HIGH)
		gpio.output(left_forward, gpio.HIGH)
	elif direction=="reverse":
		print "reverse"
		gpio.output(right_reverse,gpio.HIGH)
		gpio.output(left_reverse,gpio.HIGH)
	elif direction=="left":
		print "left"
		gpio.output(left_reverse, gpio.HIGH)
		gpio.output(right_forward, gpio.HIGH)
	elif direction=="right":
		print "right"
		gpio.output(right_reverse, gpio.HIGH)
		gpio.output(left_forward, gpio.HIGH)
		
	time.sleep(float(duration)) #leave this set until the duration ends
	pwm.stop()
	

	
gpio_init()


go("forward",2,6)
print 'forward'

go("reverse",2,4)
print 'reverse'

go("left",4,3)
print 'left'

go("right",2,6)
print 'right'

gpio.cleanup()

