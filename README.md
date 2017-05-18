# DoorButler
Raspberry Pi door audio/video intercom

## Goal
Repurpose an old RPI2/USB Camera for an automatic/smart door intercom (audio intercom and one way video)

## Libraries (Credits)
https://github.com/eclipse/paho.mqtt.python<br/>
https://github.com/azlux/pymumble<br/>
https://github.com/larsimmisch/pyalsaaudio<br/>

## Hardware
Raspberry Pi 2<br/>
USB Camera with Microphone<br/>

## Installation
Install motion <http://lavrsen.dk/foswiki/bin/view/Motion/WebHome><br/>
Install mumble-server <http://wiki.mumble.info/wiki/Installing_Mumble><br/>

## Configuration
Find the ALSA recording device:<br/>
arecord -l<br/>

In my case, I get this:
**** List of CAPTURE Hardware Devices ****
card 1: U0x46d0x8ce [USB Device 0x46d:0x8ce], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0



