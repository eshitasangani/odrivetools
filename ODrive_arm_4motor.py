import odrive
from odrive.enums import *
import time
import keyboard
import curses
import serial

# try:
# 	usb = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
# 	usb.reset_input_buffer()
# except:
# 	print("ERROR - Could not open serial port.")
# 	print("exit")
# 	exit()

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

FWD = 2
REV = 3

GPIO.setup(FWD, GPIO.OUT)
GPIO.setup(REV, GPIO.OUT)

SERIAL1 = "206534845748" #front wheels
SERIAL2 = "206A349E5748" #back wheels
SERIAL3 = "206A34A05748" #Main arm
SERIAL4 = "" #Wrist

# Sets max current commanded and max current margin to the respective values for each motor
def setCurrentLimits(max_current_commanded, max_current_measured, odrv1, odrv2):
    odrv1.axis0.motor.config.current_lim        = max_current_commanded
    odrv1.axis0.motor.config.current_lim_margin = max_current_measured
    odrv1.axis1.motor.config.current_lim        = max_current_commanded
    odrv1.axis1.motor.config.current_lim_margin = max_current_measured

    odrv2.axis0.motor.config.current_lim        = max_current_commanded
    odrv2.axis0.motor.config.current_lim_margin = max_current_measured
    odrv2.axis1.motor.config.current_lim        = max_current_commanded
    odrv2.axis1.motor.config.current_lim_margin = max_current_measured

    odrv3.axis0.motor.config.current_lim        = 8
    odrv3.axis0.motor.config.current_lim_margin = 8
    odrv3.axis1.motor.config.current_lim        = 8
    odrv3.axis1.motor.config.current_lim_margin = 8

    odrv4.axis0.motor.config.current_lim        = 8
    odrv4.axis0.motor.config.current_lim_margin = 8
    odrv4.axis1.motor.config.current_lim        = 8
    odrv4.axis1.motor.config.current_lim_margin = 8

# Sets velocity control for all motors
def setControlMode(odrv1, odrv2, odrv3, odrv4):
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
    odrv3.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    odrv3.axis0.controller.input_vel           = 0
    print("Odrv3 Axis0 set to position control")

    odrv3.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv3.axis1.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    odrv3.axis1.controller.input_pos           = 0
    print("Odrv3 Axis1 set to position control")

    odrv4.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv4.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv4.axis0.controller.input_vel           = 0
    print("Odrv4 Axis0 set to velocity control")

    odrv4.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv4.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv4.axis1.controller.input_vel           = 0
    print("Odrv4 Axis1 set to velocity control")


# Sets the velocity of each axis to the respective setpoint by ramping
def set_Velocity(vel_setpoint_axis0, vel_setpoint_axis1, odrv1, odrv2, turning):
    print("Setting Velocity....")
    if(turning):
        while((odrv1.axis0.controller.input_vel != vel_setpoint_axis0) or (odrv1.axis1.controller.input_vel != vel_setpoint_axis1) or (odrv2.axis0.controller.input_vel != vel_setpoint_axis0) or (odrv2.axis1.controller.input_vel != vel_setpoint_axis1)):
            
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
            if   (odrv2.axis0.controller.input_vel < vel_setpoint_axis0): 
                print("Increasing odrv2 axis0")
                odrv2.axis0.controller.input_vel = odrv2.axis0.controller.input_vel + 1
            elif (odrv2.axis0.controller.input_vel > vel_setpoint_axis0):
                print("Decreasing odrv2 axis0")
                odrv2.axis0.controller.input_vel = odrv2.axis0.controller.input_vel - 1
            
            #Odrv2 axis1
            if   (odrv2.axis1.controller.input_vel < vel_setpoint_axis1):
                print("Increasing odrv2 axis1")
                odrv2.axis1.controller.input_vel = odrv2.axis1.controller.input_vel + 1
            elif (odrv2.axis1.controller.input_vel > vel_setpoint_axis1):
                print("Decreasing odrv2 axis1")
                odrv2.axis1.controller.input_vel = odrv2.axis1.controller.input_vel - 1 
            
            time.sleep(0.1) #Delay the ramp up by a tenth of a second
    else:
        while((odrv1.axis0.controller.input_vel != vel_setpoint_axis0) and (odrv1.axis1.controller.input_vel != vel_setpoint_axis1) and (odrv2.axis0.controller.input_vel != vel_setpoint_axis0) and (odrv2.axis1.controller.input_vel != vel_setpoint_axis1)):
            
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
            if   (odrv2.axis0.controller.input_vel < vel_setpoint_axis0): 
                print("Increasing odrv2 axis0")
                odrv2.axis0.controller.input_vel = odrv2.axis0.controller.input_vel + 1
            elif (odrv2.axis0.controller.input_vel > vel_setpoint_axis0):
                print("Decreasing odrv2 axis0")
                odrv2.axis0.controller.input_vel = odrv2.axis0.controller.input_vel - 1
            
            #Odrv2 axis1
            if   (odrv2.axis1.controller.input_vel < vel_setpoint_axis1):
                print("Increasing odrv2 axis1")
                odrv2.axis1.controller.input_vel = odrv2.axis1.controller.input_vel + 1
            elif (odrv2.axis1.controller.input_vel > vel_setpoint_axis1):
                print("Decreasing odrv2 axis1")
                odrv2.axis1.controller.input_vel = odrv2.axis1.controller.input_vel - 1 
            
            time.sleep(0.1) #Delay the ramp up by a tenth of a second
            
    print("Velocity set!")
    
#Stops all motors by ramping down
def stopDrive(odrv1, odrv2):
    set_Velocity(0,0, odrv1, odrv2, True)

# Return true if any axis has a non-zero velocity
def isMoving(odrv1, odrv2):
    return odrv1.axis0.controller.input_vel != 0 or odrv1.axis1.controller.input_vel != 0 or odrv2.axis0.controller.input_vel != 0 or odrv2.axis1.controller.input_vel != 0  

# Return true if moving forward
def isMovingForward(odrv1, odrv2):
    return (odrv1.axis0.controller.input_vel < 0 and odrv1.axis1.controller.input_vel > 0 and odrv2.axis0.controller.input_vel < 0 and odrv2.axis1.controller.input_vel > 0)

# Return true if moving backward
def isMovingBackward(odrv1, odrv2):
    return (odrv1.axis0.controller.input_vel > 0 and odrv1.axis1.controller.input_vel < 0 and odrv2.axis0.controller.input_vel > 0 and odrv2.axis1.controller.input_vel < 0)

# Return true if moving left
def isMovingLeft(odrv1, odrv2):
    return (odrv1.axis0.controller.input_vel < 0 and odrv1.axis1.controller.input_vel < 0 and odrv2.axis0.controller.input_vel < 0 and odrv2.axis1.controller.input_vel < 0)

# Return true if moving right
def isMovingRight(odrv1, odrv2):
    return (odrv1.axis0.controller.input_vel > 0 and odrv1.axis1.controller.input_vel > 0 and odrv2.axis0.controller.input_vel > 0 and odrv2.axis1.controller.input_vel > 0)

# Prints the motor(s) that have current limit violations
def checkCurrentLimitViolation(odrv1, odrv2):
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
    if (not error):
        print("No current limit violation detected")

# Returns the highest measured current from all 6 motors
def getMaxCurrentMeasured(odrv1, odrv2):
    return max(odrv1.axis0.motor.current_control.Iq_measured, odrv1.axis1.motor.current_control.Iq_measured, odrv2.axis0.motor.current_control.Iq_measured, odrv2.axis1.motor.current_control.Iq_measured)

# Returns the highest commanded current from all 6 motors
def getMaxCurrentCommanded(odrv1, odrv2):
    return max(odrv1.axis0.motor.current_control.Iq_setpoint, odrv1.axis1.motor.current_control.Iq_setpoint, odrv2.axis0.motor.current_control.Iq_setpoint, odrv2.axis1.motor.current_control.Iq_setpoint)

CONTROL_DRIVES       = True
CONTROL_ARM          = False
CONTROL_ARM_MAIN     = False
CONTROL_ARM_WRIST    = False
CONTROL_ARM_SHOULDER = False
CONTROL_ARM_ELBOW    = False
CONTROL_ARM_TILT     = False
CONTROL_ARM_ROTATE   = False

if __name__ == '__main__':

    print("Finding odrives")
    odrv1 = odrive.find_any(serial_number = SERIAL1)
    print("Odrive 1 found")

    odrv2 = odrive.find_any(serial_number = SERIAL2)
    print("Odrive 2 found")

    odrv3 = odrive.find_any(serial_number = SERIAL3)
    print("Odrive 3 found")

    odrv4 = odrive.find_any(serial_number = SERIAL4)
    print("Odrive 4 found")


    stdscr = curses.initscr()
    print("Terminal independent input initialized")

    curses.start_color()
    curses.noecho() # Stop keystrokes from outputting garbage into the terminal
    curses.cbreak() # Prevent the enter key from having to be pressed
    stdscr.keypad(True) # Allow for convenient key macros
    
    setControlMode(odrv1, odrv2, odrv3, odrv4) #Set velocity control for both axis right now

    # Set current limits
    print("Setting current limits to 9A commanded and 10A margin")
    setCurrentLimits(9, 10, odrv1, odrv2, odrv3, odrv4)

    # Main polling loop
    try:
        while (1):
            command = stdscr.getch() # Wait for a command

            ## LED COMMANDS
            # if command == ord('r'):
            #     usb.write(b'RED')
            #     print("RED SET")
            # elif command == ord('g'):
            #     usb.write(b'GREEN')
            #     print("GREEN SET")
            # elif command == ord('b'):
            #     print("BLUE SET")
            #     usb.write(b'BLUE')
            # elif command == ord('p'):
            #     print("OFF SET")
            #     usb.write(b'OFF')
            # elif command == ord('f'):
            #     print("FLASH SET")
            #     usb.write(b'FLASH')
            # elif command == ord('d'):
            #     print("SOLID SET")
            #     usb.write(b'SOLID')


            #Move forward
            if command == curses.KEY_UP:
                if(CONTROL_DRIVES):
                    #Block for velocity input
                    print("Enter Velocity:")
                    vel = int(stdscr.getstr(2))
                    while(vel > 40):
                        print("Velocity too high, enter something lower")
                        vel = int(stdscr.getstr(2))
                    if(not isMovingForward(odrv1, odrv2)):
                        stopDrive(odrv1, odrv2) # Stop the motors if we are not already going forwards
                    set_Velocity(vel*-1, vel, odrv1, odrv2, False)
                else:
                    print("Drive control not set!")
                
            #Move back
            elif command == curses.KEY_DOWN:
                if(CONTROL_DRIVES):
                    #Block for velocity input
                    print("Enter Velocity:")
                    vel = int(stdscr.getstr(2))
                    while(vel > 40):
                        print("Velocity too high, enter something lower")
                        vel = int(stdscr.getstr(2))
                    if(not isMovingBackward(odrv1, odrv2)):
                        stopDrive(odrv1, odrv2) # Stop the motors if we are not already going backwards
                    set_Velocity(vel, vel*-1, odrv1, odrv2, False)
                else:
                    print("Drive control not set!")
    
            # Move left
            elif command == curses.KEY_LEFT:
                if(CONTROL_DRIVES):
                    print("Enter turn type (p = point, w=swing)")
                    turn_type = stdscr.getch()
                    if (turn_type == ord('w')):
                        #Block for velocity input
                        print("Enter Velocity:")
                        vel = int(stdscr.getstr(2))
                        while(vel > 40):
                            print("Velocity too high, enter something lower")
                            vel = int(stdscr.getstr(2))
                        stopDrive(odrv1, odrv2) # Stop the motors if we are not already going left
                        set_Velocity(vel*-1, vel*2, odrv1, odrv2, True)
                    elif (turn_type == ord('p')):
                        #Block for velocity input
                        print("Enter Velocity:")
                        vel = int(stdscr.getstr(2))
                        while(vel > 40):
                            print("Velocity too high, enter something lower")
                            vel = int(stdscr.getstr(2))
                        if(not isMovingLeft(odrv1, odrv2)):
                            stopDrive(odrv1, odrv2) # Stop the motors if we are not already going left
                        set_Velocity(vel*-1, vel*-1, odrv1, odrv2, False)
                    else:
                        print("Try again with a valid turn type")
                elif(CONTROL_ARM):
                    if(CONTROL_ARM_MAIN):
                        if(CONTROL_ARM_ELBOW):
                            print("Increasing position CCW...")
                            odrv3.axis0.controller.input_pos = odrv3.axis0.controller.input_pos + 1
                        elif(CONTROL_ARM_SHOULDER):
                            print("Increasing position CCW...")
                            odrv3.axis1.controller.input_pos = odrv3.axis1.controller.input_pos - 1
                        else:
                            print("Please set control to elbow or shoulder!")
                    elif(CONTROL_ARM_WRIST):
                        if(CONTROL_ARM_TILT):
                            print("Increasing position CCW...")
                            odrv4.axis1.controller.input_vel = 4 
                        elif(CONTROL_ARM_ROTATE):
                            print("Increasing position CCW...")
                            odrv4.axis0.controller.input_vel = 4 
                        else:
                            print("Please set control to tilt or rotate!")    
                    else:
                        print("Valid arm control not set!")
                    
                
            # Move right
            elif command == curses.KEY_RIGHT:
                if(CONTROL_DRIVES):
                    print("Enter turn type (p = point, w=swing)")
                    turn_type = stdscr.getch()
                    if (turn_type == ord('w')):
                        #Block for velocity input
                        print("Enter Velocity:")
                        vel = int(stdscr.getstr(2))
                        while(vel > 40):
                            print("Velocity too high, enter something lower")
                            vel = int(stdscr.getstr(2))
                        stopDrive(odrv1, odrv2) # Stop the motors if we are not already going right
                        set_Velocity(vel*-2, vel, odrv1, odrv2, True)
                    elif (turn_type == ord('p')):
                        #Block for velocity input
                        print("Enter Velocity:")
                        vel = int(stdscr.getstr(2))
                        while(vel > 40):
                            print("Velocity too high, enter something lower")
                            vel = int(stdscr.getstr(2))
                        if(not isMovingLeft(odrv1, odrv2)):
                            stopDrive(odrv1, odrv2) # Stop the motors if we are not already going left
                        set_Velocity(vel, vel, odrv1, odrv2, False)
                    else:
                        print("Try again with a valid turn type")
                elif(CONTROL_ARM):
                    if(CONTROL_ARM_MAIN):
                        if(CONTROL_ARM_ELBOW):
                            print("Increasing position CW...")
                            odrv3.axis0.controller.input_pos = odrv3.axis0.controller.input_pos - 1
                        elif(CONTROL_ARM_SHOULDER):
                            print("Increasing position CW...")
                            odrv3.axis1.controller.input_pos = odrv3.axis1.controller.input_pos + 1
                        else:
                            print("Please set control to elbow or shoulder!")
                    elif(CONTROL_ARM_WRIST):
                        if(CONTROL_ARM_TILT):
                            print("Increasing position CW...")
                            odrv4.axis1.controller.input_vel = -4 # TODO: Check if the directions match
                        elif(CONTROL_ARM_ROTATE):
                            print("Increasing position CW...")
                            odrv4.axis0.controller.input_vel = -4 # TODO: Check if the directions match
                        else:
                            print("Please set control to tilt or rotate!")    
                    else:
                        print("Valid arm control not set!")
                
                
            # Calibration command
            elif command == ord('c'):
                print("Attempting calibration...")
                if(isMoving(odrv1, odrv2)):
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
                    odrv4.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                    while (odrv4.axis0.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv4 axis0...")
                    odrv4.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                    while (odrv4.axis1.current_state != AXIS_STATE_IDLE):
                        time.sleep(1)
                        print("Calibrating odrv4 axis1...")
                    
                    setControlModeVelocity(odrv1, odrv2) #After calibration, set all motors back to velocity control
            
            elif command == ord('m'):
                print("Stopping rover")
                stopDrive(odrv1, odrv2)
                print("Choose Drives (d) or Arm (a)")
                CONTROL = stdscr.getch()
                if(CONTROL == ord('d')):
                    CONTROL_DRIVES    = True
                    CONTROL_ARM       = False
                    CONTROL_ARM_WRIST = False
                    CONTROL_ARM_MAIN  = False
                    print("Drives control set")
                elif(CONTROL == ord('a')):
                    print("Choose Main arm (m) or wrist (w)")
                    CONTROL_ARM    = True
                    CONTROL_DRIVES = False
                    CONTROL = stdscr.getch()
                    if(CONTROL == ord('m')):
                        CONTROL_ARM_MAIN  = True
                        CONTROL_ARM_WRIST = False
                        print("Setting control to main arm")
                    elif(CONTROL == ord('w')):
                        CONTROL_ARM_WRIST = True
                        CONTROL_ARM_MAIN  = False
                        print("Setting control to wrist")
                    else:
                        CONTROL_ARM_MAIN  = False
                        CONTROL_ARM_WRIST = False
                        CONTROL_ARM       = False
                        CONTROL_DRIVES    = True
                        print("Invalid control mode entered, setting control to drives")
                else:
                    CONTROL_ARM_MAIN  = False
                    CONTROL_ARM_WRIST = False
                    CONTROL_ARM       = False
                    CONTROL_DRIVES    = True
                    print("Invalid control mode entered, setting control to drives")

            # Stop command or set to shoulder
            elif command == ord('s'):
                if(CONTROL_ARM and CONTROL_ARM_MAIN):
                    CONTROL_ARM_SHOULDER = True
                    CONTROL_ARM_ELBOW    = False
                    print("Setting control to arm shoulder")
                elif(CONTROL_ARM and CONTROL_ARM_WRIST):
                    odrv4.axis0.controller.input_vel = 0
                    odrv4.axis1.controller.input_vel = 0
                    print("Stopping wrist")
                else:
                    print("Stopping motor...")
                    stopDrive(odrv1, odrv2)
                
            # Set control to elbow
            elif command == ord('e'):
                if(CONTROL_ARM and CONTROL_ARM_MAIN):
                    CONTROL_ARM_ELBOW    = True
                    CONTROL_ARM_SHOULDER = False
                    print("Setting control to arm elbow")
                else:
                    print("Arm main control not set!")

            # Set control to wrist tilt
            elif command == ord('t'):
                if(CONTROL_ARM and CONTROL_ARM_WRIST):
                    CONTROL_ARM_TILT   = True
                    CONTROL_ARM_ROTATE = False
                    print("Setting control to wrist tilt")
                else:
                    print("Arm wrist control not set!")

            # Setting control to wrist rotate
            elif command == ord('r'):
                if(CONTROL_ARM and CONTROL_ARM_ROTATE):
                    CONTROL_ARM_TILT   = False
                    CONTROL_ARM_ROTATE = True
                    print("Setting control to wrist rotate")
                else:
                    print("Arm wrist control not set!")

            elif command == ord('i'):
                if(CONTROL_ARM):
                    print("Attempting to straighten")
                    odrv3.axis0.controller.input_pos = 0
                    odrv3.axis1.controller.input_pos = 0
                    odrv4.axis0.controller.input_pos = 0
                    odrv4.axis1.controller.input_pos = 0
                else:
                    print("Arm control not set!")

            elif command == ord('l'):
                print("Closing end effector.")
                GPIO.output(FWD, GPIO.HIGH)
                GPIO.output(REV, GPIO.LOW)
            
            elif command == ord('o'):
                print("Opening end effector.")
                GPIO.output(FWD, GPIO.LOW)
                GPIO.output(REV, GPIO.HIGH)

            elif command == ord('p'):
                print("Stopping end effector.")
                GPIO.output(FWD, GPIO.LOW)
                GPIO.output(REV, GPIO.LOW)
            

            print("Looking for new command")
    
    except:
        # shut down 
        odrv4.axis0.controller.input_vel = 0
        odrv4.axis1.controller.input_vel = 0
        stopDrive(odrv1, odrv2)
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()