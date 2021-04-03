# Cyber plant files
* Make sure you have the directory: "/home/pi/Data/" created in your rpi.

Two variants are developed for this project. The first has 2 cameras, one in the side and another one on the top.

* For 1 camera variant the pinout is the following:

  * Side camera motor

|**rpi pin#**|**rpi SW pin#**|**Bigeasy driver**|
|----|----|----|
|29|5|EN|
|31|6|MS1|
|33|13|MS2|
|35|19|MS3|
|37|26|DR|
|30|GND|Bigeasy driver GND|
|36|16|ST|
|34|GND|Switch1|
|38|20|Switch1|
  
  * Top motor

|**rpi pin#**|**rpi SW pin#**|**Bigeasy driver**|
|----|----|----|
|11|17|EN|
|13|27|MS1|
|15|22|MS2|
|19|10|MS3|
|21|9|DR|
|14|GND|Bigeasy driver GND|
|18|24|ST|
|20|GND|Switch1|
|22|25|Switch1|

* For 2 camera variant the pinout for each rpi the following:

|**rpi pin#**|**rpi SW pin#**|**Bigeasy driver**|
|----|----|----|
|29|5|EN|
|31|6|MS1|
|33|13|MS2|
|35|19|MS3|
|37|26|DR|
|30|GND|Bigeasy driver GND|
|36|16|ST|
|34|GND|Switch1|
|38|20|Switch1|
* SW pin # is the number used in the scripts.

* When setting the serial port, disable the console for serial messages and enable the serial port using the settings in sudo raspi-config.

Platform for data collection (PDC) demo:


![alt text](https://github.com/ARoS-NCSU/PlantPhenotypingPlatform/blob/main/pictures/ezgif.com-crop.gif)
