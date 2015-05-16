# -*- coding: utf-8 -*-
from tkinter import Tk, Scale, Entry, HORIZONTAL, StringVar, END, Button, messagebox, Label, PhotoImage
import os
import RPi.GPIO as gpio
from time import sleep

# Initial setup
buzzer = 8
led_1 = 13
led_2 = 19
led_3 = 26
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(buzzer, gpio.OUT)
gpio.setup(led_1, gpio.OUT)
gpio.setup(led_2, gpio.OUT)
gpio.setup(led_3, gpio.OUT)

# Servo number    GPIO number   Pin in P1 header
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


def gpio_reset_all():
    #set all GPIOs to low
    gpio.output(buzzer, gpio.LOW)
    gpio.output(led_1, gpio.LOW)
    gpio.output(led_2, gpio.LOW)
    gpio.output(led_3, gpio.LOW)


def informations():
    print("_________________________________________________________________"
          "Les angles doivent se situer entre 0 et 180 degrees"
          "Angles recommendés pour le pan: 40 à 140\n"
          "Angles recommendés pour le tilt 20 à 80"
          "'stop' pour terminer le programme \n"
          "'init' pour revenir a la position originale\n")
    print("_________________________________________________________________")


def degre_to_pulse(angle):
    # Permet de convertir un angle en une pulsation.
    # La fonction prend comme entree un entier et retourne une chaine.
    return str(int(angle * 200 / 180 + 50))


def set_servo(angle, servo):
    string = "echo " + str(servo) + "=" + degre_to_pulse(angle) + " > /dev/servoblaster"
    os.system(string)


def verif_angle(angle, min_angle, max_angle):
    if min_angle <= angle <= max_angle:
        return True
    return False


class Fenetre(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.tilt_val_init = 36
        self.pan_val_init = 77
        self.pan_min = 20
        self.pan_max = 140
        self.tilt_min = 20
        self.tilt_max = 100
        self.pas = 5

        # Full Screen
        largeur, hauteur = self.winfo_screenwidth(), self.winfo_screenheight()
        self.overrideredirect(0)
        self.geometry("%dx%d" % (700, hauteur))

        # TILT
        self.tilt_bar = Scale(self, from_=self.tilt_min, to=self.tilt_max, length=250, label='Tilt', sliderlength=20,
                              orient=HORIZONTAL,
                              command=self.update_tilt)
        self.tilt_bar.set((self.tilt_max + self.tilt_min) // 2)
        self.tilt_bar.grid(row=1, column=2)

        self.tilt_angle = StringVar()
        self.tilt_val = self.tilt_bar.get()

        # PAN
        self.pan_bar = Scale(self, from_=self.pan_min, to=self.pan_max, length=250, label='Pan', sliderlength=20,
                             orient=HORIZONTAL,
                             command=self.update_pan)
        self.pan_bar.set((self.pan_max + self.pan_min) // 2)
        self.pan_bar.grid(row=2, column=2)

        self.pan_angle = StringVar()
        self.pan_val = self.pan_bar.get()

        # PS3 Controller
        self.bind("<a>", self.pan_plus)
        self.bind("<d>", self.pan_moins)
        self.bind("<w>", self.tilt_plus)
        self.bind("<s>", self.tilt_moins)
        self.bind("<p>", self.pas_plus)
        self.bind("<m>", self.pas_moins)
        self.bind("<q>", self.initialiser_positon)
        self.bind("<Button-2>", self.alarm)
        self.bind("<Button-3>", self.beep)
        self.bind("<i>", self.take_picture)

        # Motor
        self.gear = 0
        self.leds = [led_1, led_2, led_3]
        self.bind("<e>", self.shift_down)
        self.bind("<r>", self.shift_up)

        # Camera
        self.capture = ''
        self.image_label = Label(self, bg='white')
        self.image_label.grid()

        # Infos
        self.pas_label = Label(self, text=str(self.pas))
        self.pas_label.grid(row=3)
        self.buzzer_state = 0

    #--------Buzzer--------
    def beep(self, event, time=100):
        self.buzzer_on()
        self.after(time, self.buzzer_off)

    def buzzer_on(self):
        gpio.output(buzzer, gpio.HIGH)
        self.buzzer_state = 1

    def buzzer_off(self):
        gpio.output(buzzer, gpio.LOW)
        self.buzzer_state = 0

    def alarm(self, event):
        if self.buzzer_state == 0:
            gpio.output(buzzer, gpio.HIGH)
            self.buzzer_state = 1
        else:
            gpio.output(buzzer, gpio.LOW)
            self.buzzer_state = 0

    #-------Camera-------
    def take_picture(self, event):
        directory = 'cd ~/Desktop'
        os.system(directory)        
        image_info = 'raspistill -vf -hf -o image.jpg -w 640 -h 480'
        os.system(image_info)
        self.beep(event)

    #-------Motor-------
    def shift_up(self, event):
        if self.gear != 3:
            self.gear += 1
            gpio.output(self.leds[self.gear-1], gpio.HIGH)

    def shift_down(self, event):
        if self.gear != 0:
            gpio.output(self.leds[self.gear-1], gpio.LOW)
            self.gear -= 1

    #-------Servos-------

    def tilt_plus(self, event):
        if verif_angle(self.tilt_val + self.pas, self.tilt_min, self.tilt_max):
            self.tilt_val += self.pas
            self.tilt_bar.set(self.tilt_val)

    def tilt_moins(self, event):
        if verif_angle(self.tilt_val - self.pas, self.tilt_min, self.tilt_max):
            self.tilt_val -= self.pas
            self.tilt_bar.set(self.tilt_val)

    def pan_plus(self, event):
        if verif_angle(self.pan_val + self.pas, self.pan_min, self.pan_max):
            self.pan_val += self.pas
            self.pan_bar.set(self.pan_val)

    def pan_moins(self, event):
        if verif_angle(self.pan_val - self.pas, self.pan_min, self.pan_max):
            self.pan_val -= self.pas * 2
            self.pan_bar.set(self.pan_val)

    def pas_plus(self, event):
        if self.pas + 1 < 21:
            self.pas += 1
            self.update_window()

    def pas_moins(self, event):
        if self.pas - 1 > 0:
            self.pas -= 1
            self.update_window()

    def update_tilt(self, x):
        if x == 0:
            pass
        set_servo(int(x), 0)
        self.tilt_val = int(x)

    def update_pan(self, x):
        if x == 0:
            pass
        set_servo(int(x), 1)
        self.pan_val = int(x)

    def update_window(self):
        self.pas_label['text'] = str(self.pas)

    def initialiser_positon(self, event):
        self.tilt_bar.set(self.tilt_val_init)
        self.pan_bar.set(self.pan_val_init)


if __name__ == "__main__":
    os_string = "sudo /home/pi/richardghirst-PiBits-bf455ee/ServoBlaster/user/servod --p1pins='11,15'"
    os.system(os_string)

    f = Fenetre()
    f.mainloop()

    os_string = "sudo killall servod"
    os.system(os_string)
    gpio_reset_all()
    print('fin du programme')
