import odrive
from odrive.enums import *
import time
import keyboard
import curses
import serial

try:
	usb = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
	usb.reset_input_buffer()
except:
	print("ERROR - Could not open serial port.")
	print("exit")
	exit()

SERIAL1 = "206534845748" #front wheels
SERIAL2 = "206A34A05748" #middle wheels
SERIAL3 = "206A349E5748" #back wheels

# Sets max current commanded and max current margin to the respective values for each motor
def setCurrentLimits(max_current_commanded, max_current_measured, odrv1, odrv2, odrv3):
    odrv1.axis0.motor.config.current_lim        = max_current_commanded
    odrv1.axis0.motor.config.current_lim_margin = max_current_measured
    odrv1.axis1.motor.config.current_lim        = max_current_commanded
    odrv1.axis1.motor.config.current_lim_margin = max_current_measured

    odrv2.axis0.motor.config.current_lim        = max_current_commanded
    odrv2.axis0.motor.config.current_lim_margin = max_current_measured
    odrv2.axis1.motor.config.current_lim        = max_current_commanded
    odrv2.axis1.motor.config.current_lim_margin = max_current_measured

    odrv3.axis0.motor.config.current_lim        = max_current_commanded
    odrv3.axis0.motor.config.current_lim_margin = max_current_measured
    odrv3.axis1.motor.config.current_lim        = max_current_commanded
    odrv3.axis1.motor.config.current_lim_margin = max_current_measured

# Sets velocity control for all motors
def setControlModeVelocity(odrv1, odrv2, odrv3):
    odrv1.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv1.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv1.axis0.controller.input_vel           = 0
    print("Odrv1 Axis0 set to velocity control")

    odrv1.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv1.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv1.axis1.controller.input_vel           = 0
    print("Odrv1 Axis1 set to velocity control")

    odrv2.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv2.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv2.axis0.controller.input_vel           = 0
    print("Odrv2 Axis0 set to velocity control")

    odrv2.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv2.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv2.axis1.controller.input_vel           = 0
    print("Odrv2 Axis1 set to velocity control")

    odrv3.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv3.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv3.axis0.controller.input_vel           = 0
    print("Odrv3 Axis0 set to velocity control")

    odrv3.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv3.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv3.axis1.controller.input_vel           = 0
    print("Odrv3 Axis1 set to velocity control")



# Sets the velocity of each axis to the respective setpoint by ramping
def set_Velocity(vel_setpoint_axis0, vel_setpoint_axis1, odrv1, odrv2, odrv3, swing_turn):
    print("Setting Velocity....")
    if (not swing_turn):
        while((odrv1.axis0.controller.input_vel != vel_setpoint_axis0) and (odrv1.axis1.controller.input_vel != vel_setpoint_axis1) and (odrv2.axis0.controller.input_vel != vel_setpoint_axis0) and (odrv2.axis1.controller.input_vel != vel_setpoint_axis1) and (odrv3.axis0.controller.input_vel != vel_setpoint_axis0) and (odrv3.axis1.controller.input_vel != vel_setpoint_axis1)):
            
            #Odrv1 axis0
            if   (odrv1.axis0.controller.input_vel < vel_setpoint_axis0): 
                print("Increasing odrv1 axis0")
                odrv1.axis0.controller.input_vel = odrv1.axis0.controller.input_vel + 1
            elif (odrv1.axis0.controller.input_vel > vel_setpoint_axis0):
                print("Decreasing odrv1 axis0")
                odrv1.axis0.controller.input_vel = odrv1.axis0.controller.input_vel - 1
            
            #Odrv1 axis1
            if   (odrv1.axis1.controller.input_vel < vel_setpoint_axis1):
                print("Increasing odrv1 axis1")
                odrv1.axis1.controller.input_vel = odrv1.axis1.controller.input_vel + 1
            elif (odrv1.axis1.controller.input_vel > vel_setpoint_axis1):
                print("Decreasing odrv1 axis1")
                odrv1.axis1.controller.input_vel = odrv1.axis1.controller.input_vel - 1
            
            #Odrv2 axis0
            if   (odrv2.axis0.controller.input_vel < vel_setpoint_axis1): 
                print("Increasing odrv2 axis0")
                odrv2.axis0.controller.input_vel = odrv2.axis0.controller.input_vel + 1
            elif (odrv2.axis0.controller.input_vel > vel_setpoint_axis1):
                print("Decreasing odrv2 axis0")
                odrv2.axis0.controller.input_vel = odrv2.axis0.controller.input_vel - 1
            
            #Odrv2 axis1
            if   (odrv2.axis1.controller.input_vel < vel_setpoint_axis0):
                print("Increasing odrv2 axis1")
                odrv2.axis1.controller.input_vel = odrv2.axis1.controller.input_vel + 1
            elif (odrv2.axis1.controller.input_vel > vel_setpoint_axis0):
                print("Decreasing odrv2 axis1")
                odrv2.axis1.controller.input_vel = odrv2.axis1.controller.input_vel - 1
            
            #Odrv3 axis0
            if   (odrv3.axis0.controller.input_vel < vel_setpoint_axis0):
                print("Increasing odrv3 axis0")
                odrv3.axis0.controller.input_vel = odrv3.axis0.controller.input_vel + 1
            elif (odrv3.axis0.controller.input_vel > vel_setpoint_axis0):
                print("Decreasing odrv3 axis0")
                odrv3.axis0.controller.input_vel = odrv3.axis0.controller.input_vel - 1

            #Odrv3 axis1
            if   (odrv3.axis1.controller.input_vel < vel_setpoint_axis1):
                print("Increasing odrv3 axis0")
                odrv3.axis1.controller.input_vel = odrv3.axis1.controller.input_vel + 1
            elif (odrv3.axis1.controller.input_vel > vel_setpoint_axis1):
                print("Decreasing odrv3 axis1")
                odrv3.axis1.controller.input_vel = odrv3.axis1.controller.input_vel - 1
            
            time.sleep(0.1) # Delay the ramp up by a tenth of a second
    else:
        while((odrv1.axis0.controller.input_vel != vel_setpoint_axis0) or (odrv1.axis1.controller.input_vel != vel_setpoint_axis1) or (odrv2.axis0.controller.input_vel != vel_setpoint_axis0) or (odrv2.axis1.controller.input_vel != vel_setpoint_axis1) or (odrv3.axis0.controller.input_vel != vel_setpoint_axis0) or (odrv3.axis1.controller.input_vel != vel_setpoint_axis1)):
            #Odrv1 axis0
            if   (odrv1.axis0.controller.input_vel < vel_setpoint_axis0): 
                print("Increasing odrv1 axis0")
                odrv1.axis0.controller.input_vel = odrv1.axis0.controller.input_vel + 1
            elif (odrv1.axis0.controller.input_vel > vel_setpoint_axis0):
                print("Decreasing odrv1 axis0")
                odrv1.axis0.controller.input_vel = odrv1.axis0.controller.input_vel - 1
            
            #Odrv1 axis1
            if   (odrv1.axis1.controller.input_vel < vel_setpoint_axis1):
                print("Increasing odrv1 axis1")
                odrv1.axis1.controller.input_vel = odrv1.axis1.controller.input_vel + 1
            elif (odrv1.axis1.controller.input_vel > vel_setpoint_axis1):
                print("Decreasing odrv1 axis1")
                odrv1.axis1.controller.input_vel = odrv1.axis1.controller.input_vel - 1
            
            #Odrv2 axis0
            if   (odrv2.axis0.controller.input_vel < vel_setpoint_axis1): 
                print("Increasing odrv2 axis0")
                odrv2.axis0.controller.input_vel = odrv2.axis0.controller.input_vel + 1
            elif (odrv2.axis0.controller.input_vel > vel_setpoint_axis1):
                print("Decreasing odrv2 axis0")
                odrv2.axis0.controller.input_vel = odrv2.axis0.controller.input_vel - 1
            
            #Odrv2 axis1
            if   (odrv2.axis1.controller.input_vel < vel_setpoint_axis0):
                print("Increasing odrv2 axis1")
                odrv2.axis1.controller.input_vel = odrv2.axis1.controller.input_vel + 1
            elif (odrv2.axis1.controller.input_vel > vel_setpoint_axis0):
                print("Decreasing odrv2 axis1")
                odrv2.axis1.controller.input_vel = odrv2.axis1.controller.input_vel - 1
            
            #Odrv3 axis0
            if   (odrv3.axis0.controller.input_vel < vel_setpoint_axis0):
                print("Increasing odrv3 axis0")
                odrv3.axis0.controller.input_vel = odrv3.axis0.controller.input_vel + 1
            elif (odrv3.axis0.controller.input_vel > vel_setpoint_axis0):
                print("Decreasing odrv3 axis0")
                odrv3.axis0.controller.input_vel = odrv3.axis0.controller.input_vel - 1

            #Odrv3 axis1
            if   (odrv3.axis1.controller.input_vel < vel_setpoint_axis1):
                print("Increasing odrv3 axis0")
                odrv3.axis1.controller.input_vel = odrv3.axis1.controller.input_vel + 1
            elif (odrv3.axis1.controller.input_vel > vel_setpoint_axis1):
                print("Decreasing odrv3 axis1")
                odrv3.axis1.controller.input_vel = odrv3.axis1.controller.input_vel - 1
            
            time.sleep(0.1) # Delay the ramp up by a tenth of a second
        
    print("Velocity set!")

#Stops all motors by ramping down
def stopDrive(odrv1, odrv2, odrv3):
    set_Velocity(0,0, odrv1, odrv2, odrv3)

# Return true if any axis has a non-zero velocity
def isMoving(odrv1, odrv2, odrv3):
    return odrv1.axis0.controller.input_vel != 0 or odrv1.axis1.controller.input_vel != 0 or odrv2.axis0.controller.input_vel != 0 or odrv2.axis1.controller.input_vel != 0 or odrv3.axis0.controller.input_vel != 0 or odrv3.axis1.controller.input_vel != 0  

# Return true if moving forward
def isMovingForward(odrv1, odrv2, odrv3):
    return (odrv1.axis0.controller.input_vel < 0 and odrv1.axis1.controller.input_vel > 0 and odrv2.axis0.controller.input_vel > 0 and odrv2.axis1.controller.input_vel < 0 and odrv3.axis0.controller.input_vel < 0 and odrv3.axis1.controller.input_vel > 0)

# Return true if moving backward
def isMovingBackward(odrv1, odrv2, odrv3):
    return (odrv1.axis0.controller.input_vel > 0 and odrv1.axis1.controller.input_vel < 0 and odrv2.axis0.controller.input_vel < 0 and odrv2.axis1.controller.input_vel > 0 and odrv3.axis0.controller.input_vel > 0 and odrv3.axis1.controller.input_vel < 0)

# Return true if moving left
def isMovingLeft(odrv1, odrv2, odrv3):
    return (odrv1.axis0.controller.input_vel < 0 and odrv1.axis1.controller.input_vel < 0 and odrv2.axis0.controller.input_vel > 0 and odrv2.axis1.controller.input_vel < 0 and odrv3.axis0.controller.input_vel < 0 and odrv3.axis1.controller.input_vel < 0)

# Return true if moving right
def isMovingRight(odrv1, odrv2, odrv3):
    return (odrv1.axis0.controller.input_vel > 0 and odrv1.axis1.controller.input_vel > 0 and odrv2.axis0.controller.input_vel < 0 and odrv2.axis1.controller.input_vel < 0 and odrv3.axis0.controller.input_vel > 0 and odrv3.axis1.controller.input_vel > 0)

# Prints the motor(s) that have current limit violations
def checkCurrentLimitViolation(odrv1, odrv2, odrv3):
    error = False
    if (odrv1.axis0.motor.error == CURRENT_LIMIT_VIOLATION):
        stopDrive(odrv1, odrv2, odrv3)
        print("Current limit violation on front axis 0")
        error = True
    if (odrv1.axis1.motor.error == CURRENT_LIMIT_VIOLATION):
        error = True
        stopDrive(odrv1, odrv2, odrv3)
        print("Current limit violation on front axis 1")
    if (odrv2.axis0.motor.error == CURRENT_LIMIT_VIOLATION):
        error = True
        stopDrive(odrv1, odrv2, odrv3)
        print("Current limit violation on middle axis 0")
    if (odrv2.axis1.motor.error == CURRENT_LIMIT_VIOLATION):
        error = True
        stopDrive(odrv1, odrv2, odrv3)
        print("Current limit violation on middle axis 1")
    if (odrv3.axis0.motor.error == CURRENT_LIMIT_VIOLATION):
        error = True
        stopDrive(odrv1, odrv2, odrv3)
        print("Current limit violation on back axis 0")
    if (odrv3.axis1.motor.error == CURRENT_LIMIT_VIOLATION):
        error = True
        stopDrive(odrv1, odrv2, odrv3)
        print("Current limit violation on back axis 1")
    if (not error):
        print("No current limit violation detected")

# Returns the highest measured current from all 6 motors
def getMaxCurrentMeasured(odrv1, odrv2, odrv3):
    return max(odrv1.axis0.motor.current_control.Iq_measured, odrv1.axis1.motor.current_control.Iq_measured, odrv2.axis0.motor.current_control.Iq_measured, odrv2.axis1.motor.current_control.Iq_measured, odrv3.axis0.motor.current_control.Iq_measured, odrv3.axis1.motor.current_control.Iq_measured)

# Returns the highest commanded current from all 6 motors
def getMaxCurrentCommanded(odrv1, odrv2, odrv3):
    return max(odrv1.axis0.motor.current_control.Iq_setpoint, odrv1.axis1.motor.current_control.Iq_setpoint, odrv2.axis0.motor.current_control.Iq_setpoint, odrv2.axis1.motor.current_control.Iq_setpoint, odrv3.axis0.motor.current_control.Iq_setpoint, odrv3.axis1.motor.current_control.Iq_setpoint)

if __name__ == '__main__':

    print("Finding odrives")
    odrv1 = odrive.find_any(serial_number = SERIAL1)
    print("Odrive 1 found")

    odrv2 = odrive.find_any(serial_number = SERIAL2)
    print("Odrive 2 found")

    odrv3 = odrive.find_any(serial_number = SERIAL3)
    print("Odrive 3 found")

    stdscr = curses.initscr()
    print("Terminal independent input initialized")

    curses.start_color()
    curses.noecho() # Stop keystrokes from outputting garbage into the terminal
    curses.cbreak() # Prevent the enter key from having to be pressed
    stdscr.keypad(True) # Allow for convenient key macros
    
    setControlModeVelocity(odrv1, odrv2, odrv3) #Set velocity control for both axis right now

    # Set current limits
    print("Setting current limits to 9A commanded and 10A margin")
    setCurrentLimits(9, 10, odrv1, odrv2, odrv3)

    # Main polling loop
    try:
        while (1):
            command = stdscr.getch() # Wait for a command

            ## LED COMMANDS
            if command == ord('r'):
                usb.write(b'RED')
                print("RED SET")
            elif command == ord('g'):
                usb.write(b'GREEN')
                print("GREEN SET")
            elif command == ord('b'):
                print("BLUE SET")
                usb.write(b'BLUE')
            elif command == ord('p'):
                print("OFF SET")
                usb.write(b'OFF')
            elif command == ord('f'):
                print("FLASH SET")
                usb.write(b'FLASH')
            elif command == ord('d'):
                print("SOLID SET")
                usb.write(b'SOLID')

            #Move forward
            if command == curses.KEY_UP:
                #Block for velocity input
                print("Enter Velocity:")
                vel = int(stdscr.getstr(2))
                while(vel > 40):
                    print("Velocity too high, enter something lower")
                    vel = int(stdscr.getstr(2))
                if(not isMovingForward(odrv1, odrv2, odrv3)):
                    stopDrive(odrv1, odrv2, odrv3) # Stop the motors if we are not already going forwards
                set_Velocity(vel*-1, vel, odrv1, odrv2, odrv3)
            
            #Move back
            elif command == curses.KEY_DOWN:
                #Block for velocity input
                print("Enter Velocity:")
                vel = int(stdscr.getstr(2))
                while(vel > 40):
                    print("Velocity too high, enter something lower")
                    vel = int(stdscr.getstr(2))
                if(not isMovingBackward(odrv1, odrv2, odrv3)):
                    stopDrive(odrv1, odrv2, odrv3) # Stop the motors if we are not already going backwards
                set_Velocity(vel, vel*-1, odrv1, odrv2, odrv3)
            
            # Move left
            elif command == curses.KEY_LEFT:
                print("Enter turn type (p = point, w=swing)")
                turn_type = stdscr.getch()
                if (turn_type == ord('w')):
                    #Block for velocity input
                    print("Enter Velocity:")
                    vel = int(stdscr.getstr(2))
                    while(vel > 40):
                        print("Velocity too high, enter something lower")
                        vel = int(stdscr.getstr(2))
                    stopDrive(odrv1, odrv2, odrv3) # Stop the motors if we are not already going left
                    set_Velocity(vel*-1, vel*2, odrv1, odrv2, odrv3, True)
                elif (turn_type == ord('p')):
                    #Block for velocity input
                    print("Enter Velocity:")
                    vel = int(stdscr.getstr(2))
                    while(vel > 40):
                        print("Velocity too high, enter something lower")
                        vel = int(stdscr.getstr(2))
                    if(not isMovingLeft(odrv1, odrv2, odrv3)):
                        stopDrive(odrv1, odrv2, odrv3) # Stop the motors if we are not already going left
                    set_Velocity(vel*-1, vel*-1, odrv1, odrv2, odrv3, False)
                else:
                    print("Try again with a valid turn type")
                
            # Move right
            elif command == curses.KEY_RIGHT:
                print("Enter turn type (p = point, w=swing)")
                turn_type = stdscr.getch()
                print("Enter turn type (p = point, w=swing)")
                turn_type = stdscr.getch()
                if (turn_type == ord('w')):
                    #Block for velocity input
                    print("Enter Velocity:")
                    vel = int(stdscr.getstr(2))
                    while(vel > 40):
                        print("Velocity too high, enter something lower")
                        vel = int(stdscr.getstr(2))
                    stopDrive(odrv1, odrv2, odrv3) # Stop the motors if we are not already going right
                    set_Velocity(vel*-2, vel, odrv1, odrv2, odrv3, True)
                elif (turn_type == ord('p')):
                    #Block for velocity input
                    print("Enter Velocity:")
                    vel = int(stdscr.getstr(2))
                    while(vel > 40):
                        print("Velocity too high, enter something lower")
                        vel = int(stdscr.getstr(2))
                    if(not isMovingLeft(odrv1, odrv2, odrv3)):
                        stopDrive(odrv1, odrv2, odrv3) # Stop the motors if we are not already going left
                    set_Velocity(vel, vel, odrv1, odrv2, odrv3, False)
                else:
                    print("Try again with a valid turn type")
                
            # Calibration command
            elif command == ord('c'):
                print("Attempting calibration...")
                if(isMoving(odrv1, odrv2, odrv3)):
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
                    odrv2.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                    while (odrv2.axis0.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv2 axis0...")
                    odrv2.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                    while (odrv2.axis1.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv2 axis1...")
                    odrv3.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                    while (odrv3.axis0.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv3 axis0...")
                    odrv3.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                    while (odrv3.axis1.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv3 axis1...")
                    
                    #TODO: Add other motors

                    setControlModeVelocity(odrv1, odrv2, odrv3) #After calibration, set all motors back to velocity control
            
            # Stop command
            elif command == ord('s'):
                print("Stopping motor...")
                stopDrive(odrv1, odrv2, odrv3)
            
            # Check for current limit violations
            elif command == ord('e'):
                print("Checking for current limit violations....")
                checkCurrentLimitViolation(odrv1, odrv2, odrv3)

            # Error clearing command
            elif command == ord('l'):
                print("Clearing errors... Please calibrate")
                odrv1.clear_errors()
                odrv2.clear_errors()
                odrv3.clear_errors()

            # Print highest measured current
            elif command == ord('i'):
                current = getMaxCurrentMeasured(odrv1, odrv2, odrv3)
                print("Highest Measured Current: " + current)

            # Print highest commanded current
            elif command == ord('o'):
                current = getMaxCurrentCommanded(odrv1, odrv2, odrv3)
                print("Highest Commanded Current: " + current)


            print("Looking for new command")
    
    except:
        # shut down 
        stopDrive(odrv1, odrv2, odrv3)
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()