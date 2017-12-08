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
from time import sleep

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

    dev = "/dev/tty.usbserial"

    try:
      ser = serial.Serial(dev, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=1)  # open serial port
    except IOError as e:
      print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
      print "Unexpected error:", sys.exc_info()[0]
      raise

    statusText.set("Serial port '{}' is open...".format(ser.port))   # the port ID
    message.configure(fg="dark green")
    message.update()

    ser.write(format(target) + "\r\n")  # write a string
    sleep(1)                            # wait one second
    bytesToRead = ser.inWaiting()
    result = ser.read(bytesToRead)

    msg = "Sent '" + target + "' and response is: " + result
    statusText.set(msg)
    message.configure(fg="dark green")
    message.update()

    ser.close()  # close port


# def button_browse_callback():
#   """ What to do when the Browse button is pressed """
#   filename = tkFileDialog.askopenfilename()
#   entry.delete(0, END)
#   entry.insert(0, filename)
  
  # ------------------------------------------------
  
  root = Tk()
  root.title("Wieting ETC Light Controls v1.0")
  root.geometry("1000x500")
  frame = Frame(root)
  frame.pack()
  
  statusText = StringVar(root)
  statusText.set("Browse to open a file OR enter a Unison AV/Serial 1.0 command...")
  
  label = Label(root, text="Serial command or selected file/folder:")
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
