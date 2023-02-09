import odrive
from odrive.enums import *
#from time import sleep
import time
import keyboard
from multiprocessing import Queue, Value, Process

SERIAL1 = "206534845748"
SERIAL2 = "206A34A05748"
SERIAL3 = ""


def set_Velocity(vel_current, vel_setpoint, Direction, odrv1):
    vel_ramp = vel_current
    if(Master_drive_enable): #Only continue if the drive is enabled
        while((odrv1.axis0.controller.input_vel != vel_setpoint) and (odrv1.axis1.controller.input_vel != vel_setpoint)): #and (odrv2.axis0.input_vel != vel_setpoint) and (odrv2.axis1.input_vel != vel_setpoint) and (odrv3.axis0.input_vel != vel_setpoint) and (odrv3.axis1.input_vel != vel_setpoint)):
            if (Direction = 0): #Forward
                if  (odrv1.axis0.controller.input_vel < vel_setpoint):
                    odrv1.axis0.controller.input_vel = odrv1.axis0.controller.input_vel + 1

                elif (odrv1.axis0.controller.input_vel > vel_setpoint):
                    odrv1.axis0.controller.input_vel = odrv1.axis0.controller.input_vel - 1

                print("Ramping to : " + odrv1.axis0.controller.input_vel)

            elif(Direction = 1): #Backward
                if (odrv1.axis0.controller.input_vel < -vel_setpoint):
                    odrv1.axis0.controller.input_vel = odrv1.axis0.controller.input_vel + 1

                elif (odrv1.axis0.controller.input_vel > -vel_setpoint):
                    odrv1.axis0.controller.input_vel = odrv1.axis0.controller.input_vel - 1

                print("Ramping to : " + odrv1.axis0.controller.input_vel)
            
            time.sleep(0.2) #Delay the ramp up by a fifth of a second

            #TODO: Add the other motors


def Master_Poll(run_flag, enable_stop, Master_Velocity, Master_drive_enable):
    print("Finding odrives in master poll process")
    odrv1 = odrive.find_any(serial_number = SERIAL1)
    print("Odrive 1 Found in master poll process")
    #odrv2 = odrive.find_any(serial_number = SERIAL2)
    #odrv3 = odrive.find_any(serial_number = SERIAL3)
    while (run_flag):
        try:
            if keyboard.is_pressed('c'):
                #Set global stop variable before calibrating, for now just set the input velocity to 0
                odrv1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                #odrv2.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                #odrv3.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                odrv1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                #odrv2.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                #odrv3.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                while (odrv1.axis0.current_state != AXIS_STATE_IDLE or odrv1.axis1.current_state != AXIS_STATE_IDLE):
                          time.sleep(1)
                          print("Calibrating...")
                
                #After calibrating, reset the control modes
                odrv1.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv1.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                #odrv2.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                #odrv2.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                #odrv3.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                #odrv3.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                odrv1.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv1.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                #odrv2.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                #odrv2.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                #odrv3.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                #odrv3.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                print("Closed Loop and Velocity control set for all motors")

            if keyboard.is_pressed('s'):
                enable_stop = 1
            

        except KeyboardInterrupt:
            run_flag = 0
            break
            exit()
               
       
if __name__ == '__main__':

    run_flag            = Value('i', 1)
    enable_stop         = Value('i', 1)
    Master_Velocity     = Value('i', 0)
    Master_drive_enable = Value('i', 0) #When this is zero, the rover should not move no matter what
    Master_direction    = Value('i', 0) #Arbitrary direction for now

    print("Finding odrives")
    odrv1 = odrive.find_any(serial_number = SERIAL1)
    print("Odrive 1 Found")

    p0 = Process(target=Master_Poll, args=(run_flag, enable_stop, Master_Velocity, Master_drive_enable))
    
    p0.start()

    #MAIN THREAD
    #Only the main thread is allowed to contain requests for user input
    while(1):
        if keyboard.is_pressed('up'):
            time.sleep(0.01) #Try sleeping before asking for input to remove garbage string data from the input line
            #Block for velocity input
            print("Enter Velocity:")
            vel = int(input())
            Master_drive_enable = 1 #Enable driving
            vel_current         = Master_Velocity
            Master_Velocity     = vel 
            Master_direction    = 1
            set_Velocity(vel_current, Master_Velocity, Master_direction,  odrv1=odrv1)
        
        if keyboard.is_pressed('down'):
            time.sleep(0.01) #Try sleeping before asking for input to remove garbage string data from the input line
            #Block for velocity input
            print("Enter Velocity:")
            vel = int(input())
            Master_drive_enable = 1 #Enable driving
            vel_current         = Master_Velocity
            Master_Velocity     = vel 
            Master_direction    = 0
            set_Velocity(vel_current, Master_Velocity, Master_direction,  odrv1=odrv1)

    p0.join()