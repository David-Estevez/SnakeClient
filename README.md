SnakeClient
===========

Control a robotic modular snake through a GUI program.

![ScreenShot](https://raw.github.com/David-Estevez/SnakeClient/master/screenshots/screenshot.png)

 * Author: [David Estévez-Fernández](http://github.com/David-Estevez)
 * Released under GPLv3 license , Jun 2013


1. Installation
-------------------
* For running this software on your computer you just need to have installed Python
on your computer, with pyserial also installed.

* For controlling the robot, the [SnakeServer](http://github.com/David-Estevez/SnakeServer) firmware has to be installed on it.

2. Usage
------------------
* Set your robot configuration in the **config.txt** file

* Run the SnakeClient:
    * ```$ ./SnakeClient``` or ```$ python SnakeClient.py``` via terminal
    * Double click on SnakeClient.py

* To connect to the robot:
    * Turn on the robot and connect it to the computer.
    * If the serial port being used is not in the combobox, press the "Port:" button in order to refresh the list.
    * Click on 'Connect', and insert your robot password in the pop-up dialog.
    * After that, if the status does not say 'connected', reset your robot.
    * 'Connected' should appear on the status message. You can now control the robot.
