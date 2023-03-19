import time
import keyboard
import curses
import serial

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

PWM    = 2
DIR    = 3
NSLEEP = 4
NFAULT = 17
BRAKE  = 27

GPIO.setup(PWM,    GPIO.OUT)
GPIO.setup(DIR,    GPIO.OUT)
GPIO.setup(NSLEEP, GPIO.OUT)
GPIO.setup(BRAKE,  GPIO.OUT)
GPIO.setup(NFAULT, GPIO.IN)

DutyCycle = 0
p = GPIO.PWM(PWM, 1000)
p.start(DutyCycle)

GPIO.output(DIR,    0)
GPIO.output(NSLEEP, 0)
GPIO.output(BRAKE,  0)

sleep = True
DIRECTION = 0

GPIO.add_event_detect(NFAULT, callback=fault_handler, bouncetime=200)

if __name__ == '__main__':
    stdscr = curses.initscr()
    print("Terminal independent input initialized")

    curses.start_color()
    curses.noecho()     # Stop keystrokes from outputting garbage into the terminal
    curses.cbreak()     # Prevent the enter key from having to be pressed
    stdscr.keypad(True) # Allow for convenient key macros

    while(1):
        command = stdscr.getch() # Wait for a command
        print("Looking for command")
        if command == ord('s'): # Sleep control
            if(sleep):
                GPIO.output(NSLEEP, 1)
                print("Waking up driver")
            else:
                GPIO.output(NSLEEP, 0)
                print("Sleeping driver")

        elif command == ord('d'): # Direction control
            if(DIRECTION == 0):
                GPIO.output(DIR, 1)
                DIRECTION = 1
            elif(DIRECTION == 1):
                GPIO.output(DIR, 0)
                DIRECTION = 0
            print("Toggled direction")
        
        elif command == curses.KEY_UP:
            if(DutyCycle + 1 <= 100):
                DutyCycle = DutyCycle + 1
                p.ChangeDutyCycle(DutyCycle)
                print("Increasing duty cycle")
            else:
                print("Duty Cycle already at max!")
        
        elif command == curses.KEY_DOWN:
            if(DutyCycle - 1 >= 0):
                DutyCycle = DutyCycle - 1
                p.ChangeDutyCycle(DutyCycle)
                print("Decreasing duty cycle")
            else:
                print("Duty cycle already at minimum!")
        else:
            print("Enter a valid command")
        

def fault_handler(channel):
    print("NFAULT detected, waiting for reset...")
    command = stdscr.getch() # Wait for a command
    print("Looking for reset command (press R)")
    if command == ord('r'):
        DutyCycle = 0
        p.ChangeDutyCycle(DutyCycle)
        GPIO.output(4, 0)
        time.sleep(0.00003)
        GPIO.output(4, 1)
          
       





