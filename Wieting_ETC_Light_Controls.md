# Wieting ETC Light Controls

This is an application written in Python 2.7 and intended to provide control of the Wieting's ETC Unison Heritage house and stage lights.

## Graphical User Interface (GUI)

![Graphical User Interface](/ETC_Light_Control_GUI.png "Graphical User Interface")

The GUI is divided into 4 regions stacked vertically in a window.  The window regions from top-to-bottom are:

* Fader (Zone) Controls - This region features:

  * Faders implemented as sliding "scale" controls arranged to match the physical wall-mounted panels in the projection booth and backstage.  These controls can be used to set the intensity (0 is off, 100 is on-full) of individual light zones.  

  * A "Send" button below each "fader" that can be used to commit or send an intensity setting to the ETC controller and immediately change the corresponding zone's light intensity.   

  * A "Send Fader Profile" button that can be use to commit or send ALL of the fader/zone intensity settings at once.  

  * A group of 5 preset control buttons arranged to the right of the faders, matching the 5 buttons which appear on the physical, wall-mounted panels in the projection booth and backstage.

* File, Sync and Raw Command Buttons - This region, immediately below the Fader Controls features:

  * A text display/entry field box that displays the name of the last selected fader settings file, or accepts entry of a raw Unison Heritage serial control command.

  * The "Load Fader Values" button.  This button can be used to retrieve a .fad file containing a saved fader profile with intensity settings for all zones.

  * The "Save Fader Values" button.  This button can be used to save a .fad file containing the current fader profile with intensity settings for all zones.

  * The "Sync Fader Scales" button.  This button can be used to synchronize the displayed fader values with the ETC serial control values.

  * The "Send Raw Command" button.  This button can be used in conjunction wiht the text display/entry field box to send a specified serial control string directly to the ETC controller.

* Application Control Buttons - This region includes 3 buttons identifed as:

  * "Close the Serial Port" - Does just what it says, closes the ETC serial port so that future communication is disabled.

  * Help - Opens and displays this file in a browser window.

  * Exit - Closes the application.

* Response/Status Messages - This region occupies the bottom 1/3 of the window and provides text feedback to the user.  Error or Warning messages appear here in a **<span style="color:red">bold red</span>** typeface, while all other information appears in **<span style="color:green">bold green</span>** typeface.


## Workflow
  1. In the Mail.app select all messages then  **Message** | **Apply Rules**.
  Be sure to do this for all inboxes and sent mail!
  The rules move all selected, applicable messages (more than 2 weeks old) to
  mailbox: On My Mac /
  For_Archival  /Users/mark/Library/V3/ 5375A271-44A6-4E8E-
B19B-E8EC0EA9260C 
  2. Launch **EMail Archiver Pro**
  This will process all messages in the aforementioned For_Archival mailbox
  converting each to PDF along with a corresponding folder of attachments.  The
  PDFs and attachment folders are stored in
  /Users/mark/Documents/ \_Archived\_EMail_  .
  3.   Launch **Finder** then **Go** | **Connect To Server** to mount
  smb://mark@fileserver/files/ as /Volumes/files
  4. Return to this app, *McFate Household CPanel*, and click the **Backup
  \_Archived\_EMail_ from Mark's MacBook** button.
  This runs a command of the form...
  ```
  /usr/bin/python /Users/mark/Projects/Python/home_backup/home_backup/home_backup.py
  /Users/mark/Documents/_Archived_EMail_ /Volumes/files/STORAGE/_MAIL
  -c ./rsync_config.properties -m mark@tamatoledo.net -l ./home_backup.log
  --remove -u -d
  ```
  ...and moves the PDFs and corresponding folders from Step 2 to
  **//fileserver/files/STORAGE/\_MAIL/\_Archived\_EMail\_/For_ Archival.mbox/_year_/_month_** using rsync.
  5. Follow-up by deleting all files and folders from
  /Users/mark/Documents/\_Archived\_EMail_ and all mail messages from the
  'On My Mac' **For_Archival** mailbox.

  Repeat every 2-4 weeks.

# Post //fileserver/files/STORAGE/? Files to Solr

Use this command to run a Solr POST command of the form...
```
/opt/solr/bin/post -c fs-core /files/<folder>
```
...on //fileserver/files where the target _folder_ is specified using the **Browse** button and field.

Note that you may be unable to use the **Browse** button to select a target folder but you must make sure the target field contains a string matching one of these choices:
  * STORAGE/_AUDIO
  * ~~STORAGE/_BINARIES~~
  * STORAGE/_CODE
  * STORAGE/_DATA
  * STORAGE/_DOCUMENTS
  * STORAGE/_HOME_BACKUP
  * STORAGE/_IMAGES
  * STORAGE/_MAIL
  * STORAGE/_MISC
  * STORAGE/_PHOTOS
  * STORAGE/_VIDEOS
  * GENEALOGY
  * NEAT
  * ~~RESCUE~~


  Or, leave the field blank to choose ALL folders under //fileserver/files (not recommended!).
