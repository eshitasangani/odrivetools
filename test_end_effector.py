import curses

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

FWD = 2
REV = 3

GPIO.setup(FWD, GPIO.OUT)
GPIO.setup(REV, GPIO.OUT)

if __name__ == '__main__':
    stdscr = curses.initscr()
    print("Terminal independent input initialized")

    curses.start_color()
    curses.noecho() # Stop keystrokes from outputting garbage into the terminal
    curses.cbreak() # Prevent the enter key from having to be pressed
    stdscr.keypad(True) # Allow for convenient key macros

    while(1):
        command = stdscr.getch() # Wait for a command
        if command == ord('i'):
            print("Opening end effector.")
            GPIO.output(FWD, GPIO.HIGH)
            GPIO.output(REV, GPIO.LOW)
            
        elif command == ord('o'):
            print("Closing end effector.")
            GPIO.output(FWD, GPIO.LOW)
            GPIO.output(REV, GPIO.HIGH)

        elif command == ord('p'):
            print("Stopping end effector.")
            GPIO.output(FWD, GPIO.LOW)
            GPIO.output(REV, GPIO.LOW)
            
        print("Looking for new command")
