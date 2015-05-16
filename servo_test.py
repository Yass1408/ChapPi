import os

#     Servo number    GPIO number   Pin in P1 header
#          0               4             P1-7
#          1              17             P1-11
#          2              18             P1-12
#          3             21/27           P1-13
#          4              22             P1-15
#          5              23             P1-16
#          6              24             P1-18
#          7              25             P1-22

# Important de changer les valeurs de apres --p1pins=
# Dans le dernier test, j'ai pris les GPIO 17 et 22. (le GPIO 4 ne semble pas fonctionner)

os_string="sudo /home/pi/richardghirst-PiBits-bf455ee/ServoBlaster/user/servod --p1pins='11,15'"
os.system(os_string)

def degre_to_pulse(angle):	
	# Permet de convertir un angle en une pulsation.
	# Il faut que l'angle se situe entre 0 et 180 degres.
	# La pulsation retourne se situe entre 50 et 250 ms.
	# La fonction prend comme entree un entier et retourne une chaine.
	return str(int(angle * 200 / 180 + 50))

def set_servo(angle, servo):
	string="echo "+servo+"="+degre_to_pulse(angle)+" > /dev/servoblaster"                
	os.system(string)

def initialiser_positon():
	set_servo(35, '0')
	set_servo(30, '1')
print("_________________________________________________________________")
print("Entrer les angles sous la forme <pan> <tilt>. Par exemple 130 87")
print("Les angles doivent se situer entre 0 et 180 degrees")
print("Eviter les angles superieur a 168 deg pour le pan\n")
print("'stop' pour terminer le programme \n'init' pour revenir a la position originale\n")
print("_________________________________________________________________")

initialiser_positon()

while True:
	angles=input("<tilt> <pan>:  ")
	if angles=="stop":
		break
	elif angles.strip()=="init":
		initialiser_positon()
	else:
		try:
			list_angles=angles.split()
			list_angles=list(map(int, list_angles))
			set_servo(list_angles[0], '0')

			# ce if permet de controler seulement le tilt.
			if len(list_angles) == 2:
				set_servo(list_angles[1], '1')
		except:
			print("Entree invalide")

os_string="sudo killall servod"
os.system(os_string)
