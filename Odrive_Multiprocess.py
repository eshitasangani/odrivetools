import odrive
from odrive.enums import *
#from time import sleep
import time
import keyboard
from multiprocessing import Queue, Value, Process

SERIAL1 = "206534845748"
SERIAL2 = "206A34A05748"


# while True:
    if keyboard.is_pressed('up'):
 
        odrv1.axis0.controller.input_vel = 2

        odrv2.axis0.controller.input_vel = 2

        time.sleep(.5)
    if keyboard.is_pressed('down'):
   
        odrv1.axis0.controller.input_vel = -2
       
        odrv2.axis0.controller.input_vel = -2

        time.sleep(.5)
    if keyboard.is_pressed('left'):
     
        odrv1.axis0.controller.input_vel = -2

        odrv2.axis0.controller.input_vel = -2
     
        time.sleep(.5)
    if keyboard.is_pressed('right'):

        odrv1.axis0.controller.input_vel = 2
 
        odrv2.axis0.controller.input_vel = 2
       
        time.sleep(.5)


   

def Master_Poll(run_flag, enable_stop, Master_Velocity, Master_drive_enable):
    while(run_flag):
        try:
            if keyboard.is_pressed('c'):
                #Set global stop variable before calibrating, for now just set the input velocity to 0
                odrv1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                odrv2.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                odrv3.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                odrv1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                odrv2.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                odrv3.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                while (odrv1.axis0.current_state != AXIS_STATE_IDLE or odrv2.axis0.current_state != AXIS_STATE_IDLE \
                      or odrv3.axis0.current_state != AXIS_STATE_IDLE or odrv1.axis1.current_state != AXIS_STATE_IDLE or \
                      odrv2.axis1.current_state != AXIS_STATE_IDLE or odrv3.axis1.current_state != AXIS_STATE_IDLE):
                          time.sleep(0.1)
                
                #After calibrating, reset the control modes
                odrv1.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv1.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                odrv2.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv2.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                odrv3.axis0.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv3.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                odrv1.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv1.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                odrv2.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv2.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                odrv3.axis1.requested_state                = AXIS_STATE_CLOSED_LOOP_CONTROL
                odrv3.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
                print("Closed Loop and Velocity control set for all motors")

            if keyboard.is_pressed('s'):
                enable_stop = 1
            
            if keyboard.is_pressed('up'):
                #Block for velocity input
                print("Enter Velocity:")
                vel = int(input())
                Master_drive_enable = 1
                Master_Velocity = vel

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


    print("Finding 3 ODrives")
    odrv1 = odrive.find_any(serial_number = SERIAL1)
    odrv2 = odrive.find_any(serial_number = SERIAL2)
    odrv3 = odrive.find_any(serial_number = SERIAL3)
   
    p0 = Process(target=Master_Poll, args=(run_flag, enable_stop, Master_Velocity, Master_drive_enable))
    p1 = Process(target=Stop_positive, args=(run_flag, enable_stop))