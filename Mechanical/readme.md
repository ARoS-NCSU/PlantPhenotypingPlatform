
## Frame design details

* The frame was designed using the Design Architect tool, freely availble for download [here](https://promo.parker.com/promotionsite/designarchitect/us/en/home).
* The moving parts were mostly obtained [here](https://www.servocity.com/kits/) where the moving arms are based on this [kit](https://www.servocity.com/channel-slider-kit-a/).
* The design documents along with BOM can be found in this repo.
* Additional information about the motor driver can be found [here (Big Easy Driver User Manual)](https://www.schmalzhaus.com/BigEasyDriver/BigEasyDriver_UserManal.pdf) and [here (Big Easy Driver Hookup guide)](https://learn.sparkfun.com/tutorials/big-easy-driver-hookup-guide/all), but all connections are examplified in the [main](https://github.com/ARoS-NCSU/PlantPhenotypingPlatform) page of this repo. As important highlights, the manufacturer of the driver we used (Big Easy driver) recommends to solder all wires to avoid intermittent connection and consequently damage of the driver. It is important to highlight that this driver is mostly used for hobby applications, although it was handy and very useful for our research.
* Stil in terms of the driver and motor, it is important to adjust the potentiometer to the current used by your motor as shown in the first link above as well as to close the jump APWR if working with a raspberry pi 3 as we were since it is 3.3V powered.
