# py-autobrowserbot 
## Raspberry Pi Setup with Raspbian and Remote Destkop Tutorial
This tutorial was written to help network administrators setup this script on 
their Raspbery Pi (rpi) device. It is also assumed you know about remote desktops and are not afraid of the console.

## Build Instructions
1. Go to https://www.raspberrypi.org/downloads/ and download 'RASPBIAN'

2. Once you have downloaded the image, burn it to a SD Card. Note: If you have a Mac OSX Computer, download "ApplePi-Baker" and use this application to burn your image.

3. Load the SD card into the rpi. Do the appropriate setup.

4. Install the necessary libraries and reboot. We will be using "xrdp" as our remote desktop server on this device.
  ```
  $ sudo apt-get update && apt-get upgrade
  $ sudo apt-get install python3-pip python3-dev python3-setuptools git
  $ sudo apt-get install xrdp
  $ reboot
  ```

5. While the device is restarting, on your destkop computer, run your favourite remote desktop manager application. Note: If you have a Mac OSX computer, download the app "CoRD" and us it.

6. Using your desktop manager application, remotely connect to the rpi.

7. Open up a terminal and write the following code.

  ```
  $ cd ~/pi
  $ mkdir apps
  $ cd apps
  $ git clone https://github.com/bartmika/py-autobrowserbot
  $ cd py-autobrowserbot
  $ virtualenv env
  $ . env/bin/activate
  (env) sudo pip-3.2 install -r requirements.txt
  ```

8. You are now ready to run the application. Simply run the following to start:
  ```
  python3 autobrowserbot.py
  ```