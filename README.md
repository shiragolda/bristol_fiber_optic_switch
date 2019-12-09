# bristol_fiber_optic_switch
Python code to control Bristol fiber optic switch from a linux computer
Shira Jackson 2019

Code to control the Bristol Fiber Optic Switch from linux
This code is for a 4 channel switch but is easily modified for more channels. 

The Bristol Fiber Optic Switch uses USB-DIO24/37 from Measurement Computing
The pins used from the USB/DIO board are 35, 36, 37 corresponding to FIRSTPORTA

requires uldaq: https://github.com/mccdaq/uldaq
Be sure to install the prerequisites! uldaq requires UL for Linux C API

The device connects as hidraw. Check the port and give permissions.
example: sudo chmod 777 /dev/hidraw0
Without proper permissions, the code may raise a "Device not found" error.

Example usage:

fos = FOS()
fos.change_channel(2)
fos.change_channel(1)
fos.close()
