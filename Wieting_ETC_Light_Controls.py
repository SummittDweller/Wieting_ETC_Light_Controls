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

# --- Some control constants

testing = False     # Set True when testing away from the ETC controls, or False for real use.
port = "/dev/tty.usbserial"
numFaders = 7                 # The number of faders that can be controlled. Index 0 is the master.
folder = "~/Documents/FaderSettings"

# --- Define the GUI -----------------------------------------------------------------

def gui():
  
  # --- Helper functions
  
  def set_status(msg, type="INFO"):
    statusText.set(msg)
    if type == "ERROR":
      message.configure(fg="red")
    else:
      message.configure(fg="dark green")
    message.update()

  
  def read_serial_response(ser):
    if testing:
      return "Test mode is ON"
    sleep(1)  # wait one second
    bytesToRead = ser.inWaiting()
    result = ser.read(bytesToRead)
    stripped = re.sub(r"\r\n", ",", result)
    return stripped

  
  def send_serial_string(ser, code):
    if testing:
      return "Test mode is ON"
    if ser:
      try:
        ser.write(code)
        result = read_serial_response(ser)
        return result.strip(",")
      except:
        msg = "Serial connection error: {}".format(sys.exc_info()[0])
        set_status(msg, type="ERROR")
        return FALSE
    else:
      stripped = re.sub(r"\r\n", "", code)
      msg = "The port is not open.  send_serial_string() called with code '{0}'.".format(stripped)
      set_status(msg, type="ERROR")
      return FALSE


  def parse_fader_values(response):
    if testing:
      return [0,10,20,30,40,50,100]
    values = []
    for f in faders:
      values.append(0)
    RFs = response.split(",")
    pattern = re.compile(r"RF(\d*).(\d*).(\d*)")
    for setting in RFs:
      if setting:
        m = re.match(pattern, setting)
        if m:
          f = int(m.group(1))
          if f in faders:
            values[f] = int(m.group(2))
        else:
          msg = "String '{}' does not appear to be a fader setting.".format(setting)
          set_status(msg, type="ERROR")
    return values

  # --- Declare some lists
  
  faderFrames = []
  faderScales = []
  faderVals = []
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

  faders = range(numFaders)
  for f in faders:
    faderVals.append(0)

  ftypes = [('Fader files', '.fad')]

  # --- Define the callback functions
    
  def button_sync_fader_scales_callback(values, scales):
    if testing:
      values = [100,90,80,70,60,50,0]
    else:
      response = send_serial_string(ser, 'GF0\r\n')
      if response:
        values = parse_fader_values(response)
      else:
        set_status("Unable to sync fader scales.", "ERROR")
        return
    for f in faders:
      scales[f].set(values[f])


  def set_fader_callback(fadr, faders, labels):
    desc = re.sub(r"\n", " ", labels[fadr])
    lvl = faders[fadr].get()
    code = "SF{0}.{1}".format(fadr, lvl) + "\r\n"
    response = send_serial_string(ser, code)       # response here is normally EMPTY!
    msg = "Set fader '{0}' to level '{1}'.  Response: {2}".format(desc, lvl, response)
    set_status(msg)


  def button_set_fader_profile_callback(faders, faderScales):
    for f in faders:
      lvl = faderScales[f].get()
      code = "SF{0}.{1}".format(f, lvl) + "\r\n"
      response = send_serial_string(ser, code)       # response here is normally EMPTY!


  def set_preset_callback(preset, labels):
    p = preset + 1
    desc = re.sub(r"\n", " ", labels[preset])
    code = "SB{0}.2".format(p) + "\r\n"
    response = send_serial_string(ser, code)
    if response:
      msg = "Successfully toggled preset '{0}'.  Response:\n{1}".format(desc, response)
      set_status(msg)
    else:
      msg = "Toggle preset '{0}' failed!".format(desc)
      set_status(msg, type="ERROR")


  def button_help_callback():
    filename = "./Wieting_ETC_Light_Controls.md.html"
    webbrowser.open('file://' + os.path.realpath(filename))
    set_status("The help file, 'Wieting_ETC_Light_Controls.md.html' should now be visible in a new browser tab.")
    
    
  def button_send_raw_callback():
    raw = entry.get()
    code = "{0}\r\n".format(raw)
    response = send_serial_string(ser, code)
    stripped = re.sub(r"\r\n", ", ", response)
    info = (stripped[:75] + '...') if len(stripped) > 75 else stripped
    if response:
      msg = "Raw command '{0}' successfully sent.  Response:\n{1}".format(raw, info)
      set_status(msg)
    else:
      msg = "Raw command '{0}' failed!.".format(raw)
      set_status(msg, type="ERROR")


  def button_close_port_callback():
    if ser:
      ser.close()  # close port
    msg = "The serial port has been closed."
    set_status(msg)

    
  def button_load_faders_callback():
    filename = tkFileDialog.askopenfilename(initialdir=folder, filetypes = ftypes)
    with open(filename, 'r') as file:
      faderVals = [line.rstrip('\n') for line in file]
    entry.delete(0, END)
    entry.insert(0, filename)
    for f in faders[1:]:          # skip faders[0]!
      code = "SF{0}.{1}".format(f, faderVals[f]) + "\r\n"
      response = send_serial_string(ser, code)  # response here is normally EMPTY!


  def button_save_faders_callback():
    ftypes = [('Fader files', '.fad')]
    filename = tkFileDialog.asksaveasfilename(initialdir=folder,  filetypes=ftypes, defaultextension='.fad')
    with open(filename, 'w') as f:
      for v in faderVals:
        f.write("{}\n".format(v))
    entry.delete(0, END)
    entry.insert(0, filename)


  # --- Initialize the serial port ----------------------------------

  try:
    ser = serial.Serial(port, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=1)  # open serial port
    response = send_serial_string(ser, 'SC3.1\r\nGF0\r\n')
    if response:
      info = (response[:75] + '...') if len(response) > 75 else response
      msg = "Serial port '{0}' is open.\nFaders set to percentage (0-100) control mode.\n" \
            "Fader settings follow:\n{1}".format(ser.port, info)  # the port ID and response
      type = "INFO"

      faderVals = parse_fader_values(response)

    else:
      msg = "Serial port '{}' opened but it failed to initialize properly.".format(ser.port)  # the port ID
      type = "ERROR"

  except:
    ser = FALSE
    msg = "Serial connection error: {}".format(sys.exc_info()[0])
    type = "ERROR"

  # --- Build the GUI ---------------------------------------------------------
  
  window = Tk()
  window.title("Wieting ETC Light Controls v1.0")
  window.geometry("850x600")
  
  root = Frame(window, padx=10, pady=10)
  root.pack()
  
  panelFaders = Frame(root, padx=10, pady=10, relief=RAISED, bd=2)
  panelFaders.pack()
  
  fadersFrame = LabelFrame(panelFaders, text="Zones", padx=5, pady=5)
  fadersFrame.pack(side=LEFT)

  for f in faders:
    faderFrames.append(LabelFrame(fadersFrame, text=faderLabels[f], padx=20, pady=10))
    faderFrames[f].pack(side=LEFT)
    faderScales.append(Scale(faderFrames[f], from_=100, to=0))
    setFaderButtons.append(Button(faderFrames[f], text="Set", command=functools.partial(set_fader_callback, f, faderScales, faderLabels)))
    faderScales[f].set(faderVals[f])
    faderScales[f].pack()
    setFaderButtons[f].pack()

  presetsFrame = Frame(panelFaders, padx=5, pady=5)
  presetsFrame.pack(side=RIGHT)

  button_set_fader_profile = Button(presetsFrame, text="Set Fader Profile", command=functools.partial(button_set_fader_profile_callback, faders, faderScales))
  button_set_fader_profile.pack()

  sep = Frame(presetsFrame, height=1, width=80, bg="black")
  sep.pack(pady=5)

  for p in range(5):
    setPresetButtons.append(Button(presetsFrame, text=presetLabels[p], command=functools.partial(set_preset_callback, p, presetLabels)))
    setPresetButtons[p].pack()

  panelRaw = Frame(root, padx=5, pady=5, bd=5)
  panelRaw.pack()
  
  statusText = StringVar(panelRaw)
  statusText.set("Load to open a file OR enter a Unison AV/Serial 1.0 command...")
  
  label = Label(panelRaw, text="Enter a serial string (Raw Command) or Load a file to playback:", padx=10)
  label.pack()
  entry = Entry(panelRaw, width=96, justify='center')
  entry.pack()
  
  panelRawSub = Frame(panelRaw, padx=5)
  panelRawSub.pack()
  
  button_read_faders = Button(panelRawSub, text="Load Fader Values", command=button_load_faders_callback)
  button_read_faders.pack(side=LEFT)
  button_save_faders = Button(panelRawSub, text="Save Fader Values", command=button_save_faders_callback)
  button_save_faders.pack(side=LEFT)
  button_sync_fader_scales = Button(panelRawSub, text="Sync Fader Scales",
                                    command=functools.partial(button_sync_fader_scales_callback, faderVals, faderScales))
  button_sync_fader_scales.pack(side=LEFT)
  button_send_raw = Button(panelRawSub, text="Send Raw Command", command=button_send_raw_callback)
  button_send_raw.pack(side=LEFT)

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

  panelStatus = Frame(root, padx=5, pady=5)
  panelStatus.pack()
  
  message = Label(panelStatus, textvariable=statusText, padx=10, pady=5, font="Helvetica 18")
  message.pack()

  set_status(msg, type)

  mainloop()

# -----------------------------------------------------

if __name__ == "__main__":
  gui()  # run the GUI


