import odrive
from odrive.enums import *
#from time import sleep
import time
import keyboard
import curses

SERIAL1 = "206534845748"
SERIAL2 = "206A34A05748"
SERIAL3 = ""

def setCurrentLimits(max_current_commanded, max_current_measured, odrv1):
    odrv1.axis0.motor.config.current_lim        = max_current_commanded
    odrv1.axis0.motor.config.current_lim_margin = max_current_measured
    odrv1.axis1.motor.config.current_lim        = max_current_commanded
    odrv1.axis1.motor.config.current_lim_margin = max_current_measured

def setControlModeVelcity():
    odrv1.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv1.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv1.axis0.controller.input_vel           = 0
    print("Odrv1 Axis0 set to velocity control")

    odrv1.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv1.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv1.axis1.controller.input_vel           = 0
    print("Odrv1 Axis1 set to velocity control")


def set_Velocity(vel_setpoint_axis0, vel_setpoint_axis1, odrv1):
    print("Setting Velocity....")
    while((odrv1.axis0.controller.input_vel != vel_setpoint_axis0) and (odrv1.axis1.controller.input_vel != vel_setpoint_axis1)): #and (odrv2.axis0.input_vel != vel_setpoint) and (odrv2.axis1.input_vel != vel_setpoint) and (odrv3.axis0.input_vel != vel_setpoint) and (odrv3.axis1.input_vel != vel_setpoint)):
        if   (odrv1.axis0.controller.input_vel < vel_setpoint_axis0):
            print("Increasing axis0")
            odrv1.axis0.controller.input_vel = odrv1.axis0.controller.input_vel + 1

        elif (odrv1.axis0.controller.input_vel > vel_setpoint_axis0):
            print("Decreasing axis0")
            odrv1.axis0.controller.input_vel = odrv1.axis0.controller.input_vel - 1
        
        if   (odrv1.axis1.controller.input_vel < vel_setpoint_axis1):
            print("Increasing axis1")
            odrv1.axis1.controller.input_vel = odrv1.axis1.controller.input_vel + 1

        elif (odrv1.axis1.controller.input_vel > vel_setpoint_axis1):
            print("Decreasing axis1")
            odrv1.axis1.controller.input_vel = odrv1.axis1.controller.input_vel - 1
        
        time.sleep(0.1) #Delay the ramp up by a tenth of a second
        
            #TODO: Add the other motors
    print("Velocity set!")

if __name__ == '__main__':

    print("Finding odrives")
    odrv1 = odrive.find_any(serial_number = SERIAL1)
    print("Odrive 1 Found")

    stdscr = curses.initscr()
    print("Terminal independent input initialized")

    curses.start_color()
    curses.noecho() # Stop keystrokes from outputting garbage into the terminal
    curses.cbreak() # Prevent the enter key from having to be pressed
    stdscr.keypad(True) # Allow for convenient key macros
    
    setControlModeVelcity() #Set velocity control for both axis right now

    print("Setting current limits to 9A commanded and 10A margin")
    setCurrentLimits(9, 10, odrv1)

    #MAIN THREAD
    #Only the main thread is allowed to contain requests for user input
    try:
        while(1):
            command = stdscr.getch()
            if command == curses.KEY_UP:
                #Block for velocity input
                print("Enter Velocity:")
                vel = int(stdscr.getstr(2))
                set_Velocity(0, 0, odrv1)
                set_Velocity(vel, vel, odrv1)
            
            if command == curses.KEY_DOWN:
                #Block for velocity input
                print("Enter Velocity:")
                vel = int(stdscr.getstr(2))
                set_Velocity(0, 0, odrv1)
                set_Velocity(vel*-1, vel*-1, odrv1)
            
            if command == curses.KEY_LEFT:
                #Block for velocity input
                print("Enter Velocity:")
                vel = int(stdscr.getstr(2))
                set_Velocity(0, 0, odrv1)
                set_Velocity(vel*-1, vel, odrv1)
            
            if command == curses.KEY_RIGHT:
                #Block for velocity input
                print("Enter Velocity:")
                vel = int(stdscr.getstr(2))
                set_Velocity(0, 0, odrv1)
                set_Velocity(vel, vel*-1, odrv1)
            
            if command == ord('c'):
                print("Attempting calibration...")
                if(odrv1.axis0.controller.input_vel != 0):
                    print("Velocity is nonzero... stop all motors before calibrating")
                else:
                    odrv1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                    while (odrv1.axis0.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv1 axis0...")
                    odrv1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                    while (odrv1.axis1.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv1 axis1...")
                    setControlModeVelcity()
            
            if command == ord('s'):
                print("Stopping motor...")
                set_Velocity(0, 0, odrv1)
            

            print("Looking for new command")
    
    except KeyboardInterrupt:
        # shut down 
        set_Velocity(0, 0, odrv1)
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()