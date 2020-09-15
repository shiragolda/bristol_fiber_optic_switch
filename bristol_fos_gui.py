"""
Code to control the Bristol Fiber Optic Switch from linux
Shira Jackson 2019

The Bristol Fiber Optic Switch uses USB-DIO24/37 from Measurement Computing
The pins used from the USB/DIO board are 35, 36, 37 corresponding to FIRSTPORTA

requires uldaq: https://github.com/mccdaq/uldaq
Be sure to install the prerequisites! uldaq requires UL for Linux C API

The device connects as hidraw. Check the port and give permissions.
sudo chmod 777 /dev/hidraw*

"""
from __future__ import print_function
import time
from os import system
from sys import stdout

from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                   DigitalDirection, DigitalPortIoType)


import time, os
import tkinter as tk
from tkinter import font
import numpy as np
import threading


os.chdir("/home/labuser/googledrive/Calcium/code/calcium_control")

from zmqPublisher import zmqPublisher
os.chdir("/home/labuser/googledrive/Calcium/code/calcium_control/bristol_wavemeter")
from bristol_fos_v2 import FOS


class FOSGUI():
    def __init__(self):
        self.fos = FOS()
        time.sleep(0.5)
        self.fos.change_channel(2)

        self.scanning=False

        self.main_display()





    def main_display(self):
        self.root = tk.Tk()
        self.root.title("Bristol Fiber Optic Switch")


        icon = tk.PhotoImage(file='bristol_fos_icon.png')
        self.root.iconphoto(False, icon)

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=20)


        self.window = tk.Frame(width=400,height=300)
        self.window.pack()

        self.current_channel=tk.IntVar()
        self.current_channel.set(0)

        self.current_channel_text = tk.StringVar()
        self.current_channel_text.set("Current channel: %i"%self.current_channel.get())

        tk.Label(self.window,textvariable=self.current_channel_text).pack()

        # # radio buttons for manual channel selection # #
        self.buttons = []

        for i in range(4):
            self.buttons.append(tk.Radiobutton(self.window, text="Channel %i"%i, variable=self.current_channel, value=i, command=self.handle_radiobutton_click))

        for button in self.buttons:
            button.pack()

        # # scan options # #
        self.scan_start_button = tk.Button(self.window, text="Scan channels", command=self.handle_scan_start_click)
        self.scan_start_button.pack()

        self.scan_stop_button = tk.Button(self.window, text="Stop scan", command=self.handle_scan_stop_click,state=tk.DISABLED)
        self.scan_stop_button.pack()

        self.root.mainloop()

    def handle_radiobutton_click(self):
        self.fos.change_channel(self.current_channel.get())
        self.current_channel_text.set("Current channel: %i"%self.current_channel.get())


    def handle_scan_start_click(self):

        for button in self.buttons:
            button.config(state=tk.DISABLED)

        self.scan_start_button.config(state=tk.DISABLED,text="Scanning")
        self.scan_stop_button.config(state=tk.NORMAL)
        self.scanning=True


        self.scanning_thread = threading.Thread(target=self.scan_channels)
        self.scanning_thread.start()

    def handle_scan_stop_click(self):

        for button in self.buttons:
            button.config(state=tk.NORMAL)

        self.scan_stop_button.config(state=tk.DISABLED)
        self.scan_start_button.config(state=tk.NORMAL,text="Scan channels")
        self.scanning=False


    def scan_channels(self):
        while(self.scanning):
            for i in range(4):
                self.fos.change_channel(i)  #set initial input laser as the ref laser
                self.current_channel.set(i)
                self.current_channel_text.set("Current channel: %i"%self.current_channel.get())
                time.sleep(0.25)



if __name__ == '__main__':
    fosgui = FOSGUI()
    # print(fos.change_channel(0))
    # fos.close()

