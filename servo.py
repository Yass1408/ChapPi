import os

class Servo():
	def __init__(self):
		self._SERVO_PAN_VALUES={"left":"170","front":"120","right":"75"} # these values should be adjusted according to your servo setup. They define three named locations
		self._SERVO_TILT_VALUES={"up":"150", "flat":"180","down":"220"} #ditto above
		self._servo_pan=1 #the servoblaster id of the second servo
		self._servo_tilt=0# the servoblaster id of the first servo
		os_string="sudo /home/pi/PiBits/ServoBlaster/user/servod --p1pins='7,11'" #start the servod daemon and limit control to GPIO pins 7 and 11
		os.system(os_string) #write this to the system to activate the daemon
	
	def create_string(self,whichservo,whichvalue):#creates the string, makes it a little clearer
		os_string="echo "+str(whichservo)+"="+whichvalue+" > /dev/servoblaster"
		return os_string
	
	def move_servo(self,command, params=""):
		if command=="reset": # cause the pan/tilt to face the front
			action=self.create_string(str(self._servo_pan),self._SERVO_PAN_VALUES["front"])
			os.system(action)
			action=self.create_string(str(self._servo_tilt),self._SERVO_TILT_VALUES["flat"])
			os.system(action)
		elif command=="pan":
			action=self.create_string(str(self._servo_pan),self._SERVO_PAN_VALUES[params])
			os.system(action)
		elif command=="tilt":
			action=self.create_string(str(self._servo_tilt),self._SERVO_TILT_VALUES[params])
			os.system(action)
	
	def __del__(self):
		os_string="sudo killall servod"
		os.system(os_string)
