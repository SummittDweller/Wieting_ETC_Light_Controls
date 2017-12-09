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

# --- Imports -----------------------------------------------------------------------

import re
import sys
import tkFileDialog
import os.path
import webbrowser
import serial   # use 'pip install pyserial' to install
import functools
from Tkinter import *  # use 'brew install homebrew/dupes/tcl-tk' to install
from time import sleep


# --- Define the GUI -----------------------------------------------------------------

def gui():
  
  # --- Declare some lists
  
  faderFrames = []
  faderScales = []
  setFaderButtons = []
  setPresetButtons = []
  
  faderLabels = ["Master\n Control",
                 "Oleos/\nWings",
                 "House\nLights",
                 "Back of\n House",
                 "Stage\n Floods",
                 "Spots \n1 & 3",
                 "Spots \n2 & 4"]
  
  presetLabels = ["All On Full",
                  "Preshow/Credits",
                  "Feature",
                  "Undefined",
                  "All Off"]

  # --- Define the callback functions
    
  def set_fader_callback(fadr, faders, labels):
    desc = re.sub(r"\n", " ", labels[fadr])
    lvl = faders[fadr].get()
    code = "SF{0}.{1}".format(fadr, lvl) + "\r\n"
        
    if ser:
      try:
        ser.write(code)
        sleep(1)  # wait one second
        bytesToRead = ser.inWaiting()
        result = ser.read(bytesToRead)
        msg = "Set Fader for '{0}' ({1}) to Level '{2}' and the response is: {3}".format(desc, fadr, lvl, result)
        statusText.set(msg)
        message.configure(fg="dark green")
        message.update()
      except:
        msg = "Serial connection error: {}".format(sys.exc_info()[0])
        statusText.set(msg)
        message.configure(fg="red")
        message.update()
    else:
      msg = "The port is not open.  set_fader_callback() called with arguments '{0}' and '{1}'.  Level = {2}".format(fadr, desc, lvl)
    statusText.set(msg)
    message.configure(fg="red")
    message.update()


  def set_preset_callback(preset, labels):
    p = preset + 1
    desc = re.sub(r"\n", " ", labels[preset])
    code = "SB{0}.2".format(p) + "\r\n"
  
    if ser:
      try:
        ser.write(code)
        sleep(1)  # wait one second
        bytesToRead = ser.inWaiting()
        result = ser.read(bytesToRead)
        msg = "Toggled Preset '{0}' ({1}) and the response is: {1}".format(desc, p, result)
        statusText.set(msg)
        message.configure(fg="dark green")
        message.update()
      except:
        msg = "Serial connection error: {}".format(sys.exc_info()[0])
        statusText.set(msg)
        message.configure(fg="red")
        message.update()
    else:
      msg = "The port is not open.  set_preset_callback() called with arguments '{0}' and '{1}'.".format(p, desc)
      statusText.set(msg)
      message.configure(fg="red")
      message.update()


  def button_help_callback():
    filename = "./Wieting_ETC_Light_Controls.md.html"
    webbrowser.open('file://' + os.path.realpath(filename))
    statusText.set("The help file, 'Wieting_ETC_Light_Controls.md.html' should now be visible in a new browser tab.")
    message.configure(fg="dark green")

    
  def button_send_raw_callback():
    raw = entry.get()
    code = "{0}\r\n".format(raw)
    try:
      ser.write(code)
      sleep(2)  # wait two seconds
      bytesToRead = ser.inWaiting()
      result = ser.read(bytesToRead)
      msg = "Raw command '{0}' sent with response:\r\n{1}".format(raw, result)
      statusText.set(msg)
      message.configure(fg="dark green")
      message.update()
    except:
      msg = "Serial connection error: {}".format(sys.exc_info()[0])
      statusText.set(msg)
      message.configure(fg="red")
      message.update()


  def button_close_port_callback():
    if ser:
      ser.close()  # close port
    msg = "The serial port has been closed"
    statusText.set(msg)
    message.configure(fg="dark green")
    message.update()

    
  def button_browse_callback():
    filename = tkFileDialog.askopenfilename()
    entry.delete(0, END)
    entry.insert(0, filename)


  # --- Build the GUI ---------------------------------------------------------
  
  window = Tk()
  window.title("Wieting ETC Light Controls v1.0")
  window.geometry("850x750")
  
  root = Frame(window, padx=10, pady=10)
  root.pack()
  
  panelFaders = Frame(root, padx=10, pady=10, relief=RAISED, bd=2)
  panelFaders.pack()
  
  fadersFrame = LabelFrame(panelFaders, text="Zones", padx=5, pady=5)
  fadersFrame.pack(side=LEFT)

  for f in range(7):
    faderFrames.append(LabelFrame(fadersFrame, text=faderLabels[f], padx=20, pady=10))
    faderFrames[f].pack(side=LEFT)
    faderScales.append(Scale(faderFrames[f], from_=100, to=0))
    setFaderButtons.append(Button(faderFrames[f], text="Set", command=functools.partial(set_fader_callback, f, faderScales, faderLabels)))
    faderScales[f].pack()
    setFaderButtons[f].pack()

  presetsFrame = Frame(panelFaders, padx=5, pady=5)
  presetsFrame.pack(side=RIGHT)

  for p in range(5):
    setPresetButtons.append(Button(presetsFrame, text=presetLabels[p], command=functools.partial(set_preset_callback, p, presetLabels)))
    setPresetButtons[p].pack()
    
  panelRaw = Frame(root, padx=5, pady=5, bd=5)
  panelRaw.pack()
  
  statusText = StringVar(panelRaw)
  statusText.set("Browse to open a file OR enter a Unison AV/Serial 1.0 command...")
    
  label = Label(panelRaw, text="Enter a serial string (Raw Command) or Browse for a file to playback:", padx=10)
  label.pack()
  entry = Entry(panelRaw, width=96, justify='center')
  entry.pack()
  
  panelRawSub = Frame(panelRaw, padx=5)
  panelRawSub.pack()
  
  button_send_raw = Button(panelRawSub, text="Send Raw Command", command=button_send_raw_callback)
  button_send_raw.pack(side=LEFT)
  button_browse = Button(panelRawSub, text="Browse", command=button_browse_callback)
  button_browse.pack(side=LEFT)

  sep = Frame(panelRaw, height=1, width=800, bg="black")
  sep.pack(pady=10)

  panelCMD = Frame(root, padx=5, bd=2)
  panelCMD.pack()
  
  button_close_port = Button(panelCMD, text="Close the Serial Port", command=button_close_port_callback)
  button_close_port.pack(side=LEFT)
  button_help = Button(panelCMD, text="Help", command=button_help_callback)
  button_help.pack(side=LEFT)
  button_exit = Button(panelCMD, text="Exit", command=sys.exit)
  button_exit.pack(side=LEFT)

  #sep = Frame(panelCMD, height=1, width=800, bg="black", pady=5)
  #sep.pack(side=BOTTOM)

  panelStatus = Frame(root, padx=5, pady=5)
  panelStatus.pack()
  
  message = Label(panelStatus, textvariable=statusText, padx=10, pady=5)
  message.pack()
  
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
  gui()  # run the GUI

