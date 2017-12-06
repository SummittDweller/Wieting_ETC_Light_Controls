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

# import tkFileDialog
# import subprocess
# import spur  # use 'pip install spur' to install
# import json
import os.path
import webbrowser
import serial   # use 'pip install pyserial' to install
from Tkinter import *  # use 'brew install homebrew/dupes/tcl-tk' to install

# import fileinput
# import StringIO
# import glob
# import argparse
# from shutil import copyfile

def gui():
  """make the GUI version of this app"""
  
  def button_help_callback():
    """ what to do when the "Help" button is pressed """
    
    filename = "./Wieting_ETC_Light_Controls.md.html"
    webbrowser.open('file://' + os.path.realpath(filename))
    statusText.set("The help file, 'Wieting_ETC_Light_Controls.md.html' should now be visible in a new browser tab.")
    message.configure(fg="dark green")
  
  def button_send_serial_callback():
    """ what to do when the "Send Serial Test String" button is pressed """
    
    target = entry.get()
    statusText.set("button_send_serial_callback is sending '{}'...".format(target))
    message.configure(fg="red")
    message.update()

    # Open port at '9600, 8, N, 1', no timeout

    ser = serial.Serial('/dev/ttyUSB0')  # open serial port
    print(ser.name)  # check which port was really used
    ser.write(b'hello')  # write a string
    ser.close()  # close port

    # Open named port at '19200, 8, N, 1', 1s timeout

    with serial.Serial('/dev/ttyS1', 19200, timeout=1) as ser:
      x = ser.read()  # read one byte
      s = ser.read(10)  # read up to ten bytes (timeout)
      line = ser.readline()  # read a '\n' terminated line

    # Open port at '38400, 8, E, 1', non-blocking HW handshaking

    ser = serial.Serial('COM3', 38400, timeout=0,
    parity = serial.PARITY_EVEN, rtscts = 1)
    s = ser.read(100)  # read up to one hundred bytes or as much is in the buffer

    # Configuring ports later

    # Get a Serial instance and configure / open it later

    ser = serial.Serial()
    ser.baudrate = 19200
    ser.port = 'COM1'
    ser  # Serial < id = 0xa81c10, open = False > (port='COM1', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)"""
    ser.open()
    ser.is_open  # True
    ser.close()
    ser.is_open  # False

    # Also supported with context manager

    with serial.Serial() as ser:
      ser.baudrate = 19200
      ser.port = 'COM1'
      ser.open()
      ser.write(b'hello')

    statusText.set("button_send_serial_callback is complete with ser of '{}'...".format(ser))
    message.configure(fg="dark green")
  
# def button_browse_callback():
#   """ What to do when the Browse button is pressed """
#   filename = tkFileDialog.askopenfilename()
#   entry.delete(0, END)
#   entry.insert(0, filename)
  
  # ------------------------------------------------
  
  root = Tk()
  root.title("Wieting ETC Light Controls v1.0")
  root.geometry("1000x350")
  frame = Frame(root)
  frame.pack()
  
  statusText = StringVar(root)
  statusText.set("Browse to open a file OR choose an operation to perform.")
  
  label = Label(root, text="Input or selected file/folder:")
  label.pack(padx=10)
  entry = Entry(root, width=80, justify='center')
  entry.pack(padx=10)
  separator = Frame(root, height=2, bd=1, relief=SUNKEN)
  separator.pack(fill=X, padx=10, pady=5)
  
# button_browse = Button(root, text="Browse", command=button_browse_callback)
  button_send_serial = Button(root, text="Send Serial Test String", command=button_send_serial_callback)
  button_help = Button(root, text="Help", command=button_help_callback)
  button_exit = Button(root, text="Exit", command=sys.exit)
# button_browse.pack()
  button_send_serial.pack()
  button_help.pack()
  button_exit.pack()
  
  separator = Frame(root, height=2, bd=1, relief=SUNKEN)
  separator.pack(fill=X, padx=10, pady=5)
  
  message = Label(root, textvariable=statusText)
  message.pack(padx=10, pady=5)
  
  mainloop()


# -----------------------------------------------------

if __name__ == "__main__":
  gui()  # otherwise run the GUI version
