# PotholeRepair

## Setup
### Install OpenCV for Raspberry Pi
Follow the the instructions at this [link](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)

### Setup I2C for IR Temperature Sensor
* Enable I2C for Raspberry Pi
  * Run ```sudo raspi-config```
  * Under Advanced settings, select enable I2C and reboot
* Installing the bcm2835 module
  * Untar the given bcm2835 tarball
  * Enter the unpacked directory
  * Run ```./configure && make && sudo make install```
  * Run ```sudo modprobe bcm2835```
* Test installation
  * Enter the tempProgram directory and run ```./runTemp```
  * If this program returns any values, I2C is successfully setup
  
### Source Dependencies
**Should be in the virtual enviornment when installing these**
* ```pip3 install adafruit-circuitpython-motorkit```
* ```pip3 install flask```
* ```pip install "picamera[array]"```
* ```pip install opencv-contrib-python```
* ```pip install imutils```
* ```sudo apt-get install rpi.gpio```

### Create Wireless AP
* Use the following [link](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)
* **SSID must be "Repairinator" in order to work with iOS app**
  
