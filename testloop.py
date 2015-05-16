import RPi.GPIO as gpio

# INITIAL SETUP
enable_pin = 10  # Marked MOSI on the paddle board
left_forward = 5
left_reverse = 6
right_forward = 20
right_reverse = 16


def gpio_init():
    gpio.cleanup()  # clear all settings
    gpio.setmode(gpio.BCM)  # use the Broadcom numbering scheme
    gpio.setup(enable_pin, gpio.OUT)  # the enable pin that turns on the motor
    gpio.output(enable_pin, gpio.LOW)  # now set it low to make sure it's not on

    # # set the four wheels
    gpio.setup(left_forward, gpio.OUT)
    gpio.setup(left_reverse, gpio.OUT)
    gpio.setup(right_forward, gpio.OUT)
    gpio.setup(right_reverse, gpio.OUT)


def gpio_reset_all():
    # set all GPIOs to low
    gpio.output(left_forward, gpio.LOW)
    gpio.output(left_reverse, gpio.LOW)
    gpio.output(right_forward, gpio.LOW)
    gpio.output(right_reverse, gpio.LOW)

gpio_init()

direction = "i"
speed = 50
pwm = gpio.PWM(enable_pin, 50)  # 50 is the frequency

while direction:
    gpio_reset_all()

    if direction == "u":
        print("forward")
        gpio.output(right_forward, gpio.HIGH)
        gpio.output(left_forward, gpio.HIGH)
    elif direction == "j":
        print("reverse")
        gpio.output(right_reverse, gpio.HIGH)
        gpio.output(left_reverse, gpio.HIGH)
    elif direction == "k":
        print("right")
        gpio.output(left_reverse, gpio.HIGH)
        gpio.output(right_forward, gpio.HIGH)
    elif direction == "h":
        print("left")
        gpio.output(right_reverse, gpio.HIGH)
        gpio.output(left_forward, gpio.HIGH)
    elif direction == 'i':
        pwm.stop()
        pwm = gpio.PWM(enable_pin, 50)  # 50 is the frequency

    else:
        pass
    pwm.start(speed)  # a "speed" of 50, sends power exactly every second cycle
    direction = input('Entrer la direction')

gpio.cleanup()
print('fin du programme')

