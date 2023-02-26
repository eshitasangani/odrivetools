import odrive
from odrive.enums import *
import time
import curses

SERIAL1 = "xxxx" # Elbow and shoulder joint
SERIAL2 = 'xxxx' # Wrist

# Sets max current commanded and max current margin to the respective values for each motor
def setCurrentLimits(max_current_commanded, max_current_measured, odrv1, odrv2):
    odrv1.axis0.motor.config.current_lim        = max_current_commanded
    odrv1.axis0.motor.config.current_lim_margin = max_current_measured

    odrv1.axis1.motor.config.current_lim        = max_current_commanded
    odrv1.axis1.motor.config.current_lim_margin = max_current_measured

    odrv2.axis0.motor.config.current_lim        = 5
    odrv2.axis0.motor.config.current_lim_margin = 5

    odrv2.axis1.motor.config.current_lim        = 5
    odrv2.axis1.motor.config.current_lim_margin = 5
    

odrv0.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
odrv0.axis0.controller.input_vel          = 0
    

# Sets position control
def setControlModePosition(odrv1, odrv2):
    odrv1.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv1.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    odrv1.axis0.controller.input_pos           = 0
    print("Odrv1 Axis0 set to position control")

    odrv1.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv1.axis1.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    odrv1.axis1.controller.input_pos           = 0
    print("Odrv1 Axis1 set to position control")

    odrv2.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv2.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    odrv2.axis0.controller.input_pos           = 0
    print("Odrv2 Axis0 set to position control")

    odrv2.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv2.axis1.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    odrv2.axis1.controller.input_pos           = 0
    print("Odrv2 Axis1 set to position control")

# Returns the estimated velocity for the elbow joint. Positive is counter clockwise
def getElbowVelocity(odrv1):
    return odrv1.axis0.encoder.vel_estimate

# Returns the estimated velocity for the shoulder joint. Positive is clockwise
def getShoulderVelocity(odrv1):
    return odrv1.axis1.encoder.vel_estimate

if __name__ == '__main__':
    print("Finding odrives")
    odrv1 = odrive.find_any(serial_number = SERIAL1)
    print("odrv1 found")
    odrv2 = odrive.find_any(serial_number = SERIAL2)
    print("odrv2 found")

    stdscr = curses.initscr()
    print("Terminal independent input initialized")

    curses.start_color()
    curses.noecho() # Stop keystrokes from outputting garbage into the terminal
    curses.cbreak() # Prevent the enter key from having to be pressed
    stdscr.keypad(True) # Allow for convenient key macros
    
    # NOT SETTING POSITION CONTROL HERE, SET IT ONLY AFTER CALIBRATION
    #setControlModePosition(odrv1) #Set position control for both axis right now

    # Set current limits
    print("Setting current limits to 9A commanded and 10A margin")
    setCurrentLimits(9, 10, odrv1, odrv2)
    current_axis = 0
    try:
        while(1):
            command = stdscr.getch() # Wait for a command

            # Calibration command
            if command == ord('c'):
                print("Attempting calibration...")
                odrv1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                while (odrv1.axis0.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv1 axis0...")
                odrv1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                while (odrv1.axis1.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv1 axis1...")
                odrv2.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                while (odrv2.axis0.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv2 axis0...")
                odrv2.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                while (odrv2.axis1.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv2 axis1...")
                
                # After calibration, set position control again
                setControlModePosition(odrv1, odrv2)
            
            elif command == ord('e'):
                print("Setting control to elbow joint...")
                current_axis = 0
            
            elif command == ord('s'):
                print("Setting control to shoulder joint...")
                current_axis = 1
            
            elif command == ord('w'):
                print("Choose wrist tilt (t) or rotate (r)...")
                wrist = stdscr.getch() # Wait for a command
                if (wrist == ord('t')):
                    print ("Setting control to wrist tilt")
                    current_axis = 2
                elif (wrist == ord('r')):
                    print("Setting control to wrist rotate")
                    current_axis = 3
                else :
                    print("Enter a valid wrist axis")


            elif command == curses.KEY_LEFT:
                # Elbow
                if (current_axis == 0): 
                    while(getElbowVelocity(odrv1) != 0):
                        print("Waiting for joint to complete previous movement")
                    print("Increasing position CCW...")
                    odrv1.axis0.controller.input_pos = odrv1.axis0.controller.input_pos + 1
                # Shoulder
                elif (current_axis == 1):
                    while(getShoulderVelocity(odrv1) != 0):
                        print("Waiting for joint to complete previous movement")
                    print("Increasing position CCW...")
                    odrv1.axis1.controller.input_pos = odrv1.axis1.controller.input_pos - 1
                # Wrist tilt
                elif (current_axis == 2):
                    while(getWristTiltVelocity(odrv1) != 0):
                        print("Waiting for joint to complete previous movement")
                    print("Increasing position CCW...")
                    odrv1.axis0.controller.input_pos = odrv1.axis0.controller.input_pos - 1
                # TODO: Add wrist rotate here and add the rest of the wrist elsewhere
            
            elif command == curses.KEY_RIGHT:
                # Elbow
                if (current_axis == 0):
                    while(getElbowVelocity(odrv1) != 0):
                        print("Waiting for joint to complete previous movement")
                    print("Increasing position CCW...")
                    odrv1.axis0.controller.input_pos = odrv1.axis0.controller.input_pos - 1
                # Shoulder
                elif (current_axis == 1):
                    while(getShoulderVelocity(odrv1) != 0):
                        print("Waiting for joint to complete previous movement")
                    print("Increasing position CCW...")
                    odrv1.axis1.controller.input_pos = odrv1.axis1.controller.input_pos + 1

            elif command == ord('t'):
                print("Straightening... this will be fast!")
                odrv1.axis0.controller.input_pos = 0
                odrv1.axis1.controller.input_pos = 0

            elif command == ord('q'):
                print("Enter shoulder position (positive is counter clockwise)")
                s_pos = int(stdscr.getstr(2))
                s_pos = s_pos * -1
                print("Enter elbow position (positive is counter clockwise)")
                e_pos = int(stdscr.getstr(2))
                print("Setting positions")
                odrv1.axis0.controller.input_pos = e_pos
                odrv1.axis1.controller.input_pos = s_pos
            
            print("Looking for new command")

    except KeyboardInterrupt:
        odrv1.axis0.controller.input_pos = 0
        odrv1.axis1.controller.input_pos = 0
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


