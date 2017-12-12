# Wieting ETC Light Controls

This is an application written in Python 2.7 and intended to provide control of the Wieting's ETC Unison Heritage house and stage lights.

## Graphical User Interface (GUI)

![Graphical User Interface](/ETC_Light_Control_GUI.png "Graphical User Interface")

The GUI is divided into 4 regions stacked vertically in a window. The window regions from top-to-bottom are:

*   Fader (Zone) Controls

    ![Fader Controls](/ETC_Light_Control_GUI_Region_1.png "Graphical User Interface")

    This region features:

    *   Faders implemented as sliding "scale" controls arranged to match the physical wall-mounted panels in the projection booth and backstage. These controls can be used to set the intensity (0 is off, 100 is on-full) of individual light zones.

    *   A "Send" button below each "fader" that can be used to commit or send an intensity setting to the ETC controller and immediately change the corresponding zone's light intensity.

    *   A "Send Fader Profile" button that can be use to commit or send ALL of the fader/zone intensity settings at once.

    *   A group of 5 preset control buttons arranged to the right of the faders, matching the 5 buttons which appear on the physical, wall-mounted panels in the projection booth and backstage.

*   File, Sync and Raw Command Buttons

    ![File, Sync and Raw Command Buttons](/ETC_Light_Control_GUI_Region_2.png "Graphical User Interface")

    This region, immediately below the Fader Controls, features:

    *   A text display/entry field box that displays the name of the last selected fader settings file, or accepts entry of a raw Unison Heritage serial control command.

    *   The "Load Fader Values" button. This button can be used to retrieve a .fad file containing a saved fader profile with intensity settings for all zones.

    *   The "Save Fader Values" button. This button can be used to save a .fad file containing the current fader profile with intensity settings for all zones.

    *   The "Sync Fader Scales" button. This button can be used to synchronize the displayed fader values with the ETC serial control values.

    *   The "Send Raw Command" button. This button can be used in conjunction wiht the text display/entry field box to send a specified serial control string directly to the ETC controller.

*   Application Control Buttons

    ![Application Fader Control Buttons](/ETC_Light_Control_GUI_Region_3.png "Graphical User Interface")

    This region includes 3 buttons identified as:

    *   "Close the Serial Port" - Does just what it says, closes the ETC serial port so that future communication is disabled.

    *   Help - Opens and displays this file in a browser window.

    *   Exit - Closes the application.

*   Response/Status Messages

    ![Response/Status Messages](/ETC_Light_Control_GUI_Region_4.png "Graphical User Interface")

    This region occupies the bottom 1/3 of the window and provides text feedback to the user. Error or Warning messages appear here in a **<span style="color:red">bold red</span>** typeface, while all other information appears in **<span style="color:green">bold green</span>** typeface.

## Workflow
