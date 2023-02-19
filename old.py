#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""
from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math
import keyboard

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
odrv0 = odrive.find_any(#serial#);
# odrv1 = odrive.find_any(#serial#);
# odrv2 = odrive.find_any(#serial#);

# Calibrate motor and wait for it to finish
print("starting calibration...")
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while odrv0.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

while True:
    if keyboard.is_pressed('up'):
        odrv0.axis0.controller.input_vel = 1
        odrv0.axis1.controller.input_vel = 1
        odrv1.axis0.controller.input_vel = 1
        odrv1.axis1.controller.input_vel = 1
        odrv2.axis0.controller.input_vel = 1
        odrv2.axis1.controller.input_vel = 1
        time.sleep(.5)
    if keyboard.is_pressed('down'):
        odrv0.axis0.controller.input_vel = -1
        odrv0.axis1.controller.input_vel = -1
        odrv1.axis0.controller.input_vel = -1
        odrv1.axis1.controller.input_vel = -1
        odrv2.axis0.controller.input_vel = -1
        odrv2.axis1.controller.input_vel = -1
        time.sleep(.5)
    if keyboard.is_pressed('left'):
        odrv0.axis0.controller.input_vel = -1
        odrv0.axis1.controller.input_vel = 1
        odrv1.axis0.controller.input_vel = -1
        odrv1.axis1.controller.input_vel = 1
        odrv2.axis0.controller.input_vel = -1
        odrv2.axis1.controller.input_vel = 1
        time.sleep(.5)
    if keyboard.is_pressed('right'):
        odrv0.axis0.controller.input_vel = 1
        odrv0.axis1.controller.input_vel = -1
        odrv1.axis0.controller.input_vel = 1
        odrv1.axis1.controller.input_vel = -1
        odrv2.axis0.controller.input_vel = 1
        odrv2.axis1.controller.input_vel = -1
        time.sleep(.5)
         


