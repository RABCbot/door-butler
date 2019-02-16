# DoorButler
Smart video doorbell<br/>

## Goal
Device should provide following capabilities
- Video streaming - using Motion<br/>
- Mqtt support<br/>
- Presence detection<br/>
- Two way audio<br/>
- Smart voice screening (maybe using Alexa, Google or Snips)<br/>

## Current status
Unsure how to acomplish project goals<br/>
Currently focusing in simple python scripts to focus on each individual goal<br/>
Presence detection is completed, and integrates with mqtt, using a HR-SC04 ultra sensor sensor<br/> 

## Hardware
Any raspberry pi<br/>
reusing an old RPI1B<br/>
or maybe a $5 Raspberry Pi Zero W <http://www.microcenter.com/product/486575/raspberry-pi-zero-w><br/>
Playstation Eye <https://www.amazon.com/Sony-Station-Camera-Packaging-PlayStation-3/dp/B0735KNH2X/ref=pd_lpo_sbs_63_t_1?_encoding=UTF8&psc=1&refRID=TRAC8BQY437JKT9A4417><br/>
Google AIY Voice kit <http://www.microcenter.com/product/483414/aiy-voice-kit><br/>
or Adafruit MAX98357 <https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview><br />

V1: Using SIP software for the two way audio, this proved difficult and audio was not good maybe due using old RPI1b

## Libraries (Credits)
https://github.com/alaudet/hcsr04sensor<br/>
https://github.com/eclipse/paho.mqtt.python<br/>
https://github.com/azlux/pymumble<br/>
https://bitbucket.org/mkuron/sip2mumble/overview
https://github.com/larsimmisch/pyalsaaudio<br/>

## Installation
Install motion <http://lavrsen.dk/foswiki/bin/view/Motion/WebHome><br/>
(Deprecated) Install mumble-server <http://wiki.mumble.info/wiki/Installing_Mumble><br/>

