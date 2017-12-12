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

## Immediate Light Response
There are four ways to trigger an immediate response in the house/stage lights controlled by the Wieting's ETC station:

### Uniform Control of ALL zones
Trigger an immediate response in ALL zones by making a change to "Master Control" zone on the left end of the fader controls, then click the "Send" button immediately below the "Master Control" fader.  All zones will be set to the intensity specified for the "Master Control" fader.

### Change Intensity of an Individual Zone
To trigger an immediate response in a single zone make a change to the appropriate fader scale and click the "Send" button immediately below that fader.

### Change Intensity of ALL Zones
You can trigger all of the zones simultaneously so that each is set to the intensity indicated for their corresponding fader by setting the fader scales and clicking the "Send Fader Profile" button in the top/right corner of the fader controls.  This will set each zone to the intensity displayed on its fader scale.  Note that the "Master Control" fader is ignored when using this option.

### Using Preset Buttons
Five preset buttons appear to the right of the fader controls and below the "Send Fader Profile" button.  These buttons are "programmed" using the wall-mounted ETC control panels in the projection booth and/or backstage.  

To set all zones to "preset" intensities simply click the desired button.

>**Important Note**  
  Using a "preset" button will control the lights as desired, but the changes will NOT be reflected in the fader controls within this application, nor will they be reflected in the fader controls on the wall-mounted panels!  This is an ETC issue, not a problem with the software.  

## Synchronizing Fader Scales
Since it is possible to control the lights from a number of sources (the ETC wall-mounted control panels, this application, "preset" buttons in the box office), there will be times when the fader scales do NOT reflect the actual intensities of the lights.  Pressing the "Sync Fader Scales" button can help bring the fader scale controls back into "sync" with the physical light settings.

>**Important Note**  
  As stated before, using a "preset" button will control the lights as desired, but the changes will NOT be reflected in the fader controls, and the "Sync Fader Scales" button will also have NO effect. This is an ETC issue, not a problem with the software.

## Save and Replay (Load) Fader Settings
The "preset" buttons typically provide light intensities designed for different portions of a cinema/feature presentation, but this application provides a similar set of features to achieve similar results for live performances or non-cinema events.  

Use the "Save Fader Values" button to record the fader scale intensities for all zones and write them to a file, presumably one with a descriptive name.  The file will have a .fad extension and it will be stored on the host computer in a ~/FaderSettings folder.

Use the "Load Fader Values" button to read and replay fader scale intensities from a previously saved .fad file.  When this button is clicked you prompted to select an existing .fad file from ~/FolderSettings.  As soon as the file is selected and loaded the intensities within are automatically "sent" to the light controller and the lights respond.  Zones are switched in order from left-to-right as shown in the fader controls, and there may be a slight delay (roughly 1 second) between zones.

There is no need to use the "Sync Fader Scales" or "Send Fader Profiles" when you save or load (replay) a file.  

# Appendix
The following images were lifted from https://www.etcconnect.com/WorkArea/DownloadAsset.aspx?id=10737461037 and they document the raw serial commands and response codes of the ETC serial controller.

![Quick Guide Part 1](/ETC_Quick_Guide_1.png "Quick Guide")
![Quick Guide Part 2](/ETC_Quick_Guide_2.png "Quick Guide")
![Quick Guide Part 3](/ETC_Quick_Guide_3.png "Quick Guide")
![Quick Guide Part 4](/ETC_Quick_Guide_4.png "Quick Guide")
