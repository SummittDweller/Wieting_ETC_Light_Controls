#!/usr/bin/env python

"""
Wieting_ETC_Light_Controls.py - Wieting house lights control panel

Python2 script to control Wieting ETC house lights.

Basic GUI with command-line option lifted from https://acaird.github.io/2016/02/07/simple-python-gui
source.

See http://pyserial.readthedocs.io/en/latest/shortintro.html,
and https://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package, and
https://stackoverflow.com/questions/26224110/sending-byte-strings-to-serial-device
for serial port control code examples.

"""

# import subprocess
# import spur  # use 'pip install spur' to install
# import json
# import fileinput
# import StringIO
# import glob
# import argparse
# from shutil import copyfile

import sys
import tkFileDialog
import os.path
import webbrowser
import serial   # use 'pip install pyserial' to install
from Tkinter import *  # use 'brew install homebrew/dupes/tcl-tk' to install
from time import sleep

def gui():

  # --- Define the callbacks

  def button_help_callback():
    filename = "./Wieting_ETC_Light_Controls.md.html"
    webbrowser.open('file://' + os.path.realpath(filename))
    statusText.set("The help file, 'Wieting_ETC_Light_Controls.md.html' should now be visible in a new browser tab.")
    message.configure(fg="dark green")
  
  def button_select_fader1_callback():
    set_fader(1, "Oleos")

  def button_select_fader2_callback():
    set_fader(2, "House Lights")

  def button_select_fader3_callback():
    set_fader(3, "Back of House")

  def button_select_fader4_callback():
    set_fader(4, "Stage/Wing Floods")

  def button_select_fader5_callback():
    set_fader(5, "Spots 1 and 3")

  def button_select_fader6_callback():
    set_fader(6, "Spots 2 and 4")

  def button_select_all_faders_callback():
    set_fader(1, " ")
    set_fader(2, " ")
    set_fader(3, " ")
    set_fader(4, " ")
    set_fader(5, " ")
    set_fader(6, "ALL")

  def set_fader(f, desc):
    level = entry.get()
    code = "SF{0}.{1}".format(f, level) + "\r\n"
    try:
      ser.write(code)
    except:
      msg = "Serial connection error: {}".format(sys.exc_info()[0])
      statusText.set(msg)
      message.configure(fg="red")
      message.update()

    sleep(1)                      # wait one second
    bytesToRead = ser.inWaiting()
    result = ser.read(bytesToRead)
    msg = "Set Fader for '{0}' ({1}) to Level '{2}' and the response is: {3}".format(desc, f, level, result)
    statusText.set(msg)
    message.configure(fg="dark green")
    message.update()

  def button_send_raw_callback():
    raw = entry.get()
    code = "{0}\r\n".format(raw)
    try:
      ser.write(code)
    except:
      msg = "Serial connection error: {}".format(sys.exc_info()[0])
      statusText.set(msg)
      message.configure(fg="red")
      message.update()

    sleep(2)  # wait two seconds
    bytesToRead = ser.inWaiting()
    result = ser.read(bytesToRead)
    msg = "Raw command '{0}' sent with response:\r\n{1}".format(raw, result)
    statusText.set(msg)
    message.configure(fg="dark green")
    message.update()

  def button_close_port_callback():
    if ser:
      ser.close()  # close port
    msg = "The serial port has been closed"
    statusText.set(msg)
    message.configure(fg="dark green")
    message.update()

  def button_browse_callback():
    """ What to do when the Browse button is pressed """
    filename = tkFileDialog.askopenfilename()
    entry.delete(0, END)
    entry.insert(0, filename)
  
  # --- Build the GUI ---------------------------------------------
  
  root = Tk()
  root.title("Wieting ETC Light Controls v1.0")
  root.geometry("500x750")
  frame = Frame(root)
  frame.pack()
  
  statusText = StringVar(root)
  statusText.set("Browse to open a file OR enter a Unison AV/Serial 1.0 command...")
  
  label = Label(root, text="Enter a serial command (raw), fader level, or browse for a file:")
  label.pack(padx=10)
  entry = Entry(root, width=80, justify='center')
  entry.pack(padx=10)
  separator = Frame(root, height=2, bd=1, relief=SUNKEN)
  separator.pack(fill=X, padx=10, pady=5)
  
  button_browse = Button(root, text="Browse", command=button_browse_callback)
  button_send_raw = Button(root, text="Send Raw Command", command=button_send_raw_callback)
  button_select_fader1 = Button(root, text="Set Fader for Oleos (1)", command=button_select_fader1_callback)
  button_select_fader2 = Button(root, text="Set Fader for House Lights (2)", command=button_select_fader2_callback)
  button_select_fader3 = Button(root, text="Set Fader for Back of House (3)", command=button_select_fader3_callback)
  button_select_fader4 = Button(root, text="Set Fader for Stage/Wing Floods (4)", command=button_select_fader4_callback)
  button_select_fader5 = Button(root, text="Set Fader for Spots 1 & 2 (5)", command=button_select_fader5_callback)
  button_select_fader6 = Button(root, text="Set Fader for Spots 2 & 4 (6)", command=button_select_fader6_callback)
  button_select_all_faders = Button(root, text="Set All Faders (1-6)", command=button_select_all_faders_callback)
  button_close_port = Button(root, text="Close the Serial Port", command=button_close_port_callback)
  button_help = Button(root, text="Help", command=button_help_callback)
  button_exit = Button(root, text="Exit", command=sys.exit)
  button_browse.pack()
  button_send_raw.pack()
  button_select_fader1.pack()
  button_select_fader2.pack()
  button_select_fader3.pack()
  button_select_fader4.pack()
  button_select_fader5.pack()
  button_select_fader6.pack()
  button_select_all_faders.pack()
  button_close_port.pack()
  button_help.pack()
  button_exit.pack()
  
  separator = Frame(root, height=2, bd=1, relief=SUNKEN)
  separator.pack(fill=X, padx=10, pady=5)
  
  message = Label(root, textvariable=statusText)
  message.pack(padx=10, pady=5)
  
  # --- Initialize the serial port ----------------------------------
  dev = "/dev/tty.usbserial"

  try:
    ser = serial.Serial(dev, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=1)  # open serial port
    statusText.set("Serial port '{}' is open...".format(ser.port))  # the port ID
    message.configure(fg="dark green")
    message.update()
  except:
    ser = FALSE
    msg = "Serial connection error: {}".format(sys.exc_info()[0])
    statusText.set(msg)
    message.configure(fg="red")
    message.update()
  
  mainloop()


# -----------------------------------------------------

if __name__ == "__main__":
  gui()  # run the GUI version
