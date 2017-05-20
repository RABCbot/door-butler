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
arecord -L<br/>

In my case, I get a list of all devices, with the USB Microphone listed as:
null
    Discard all samples (playback) or generate zero samples (capture)
default:CARD=U0x46d0x8ce
    USB Device 0x46d:0x8ce, USB Audio
    Default Audio Device
hw:CARD=U0x46d0x8ce,DEV=0
    USB Device 0x46d:0x8ce, USB Audio
    Direct hardware device without any conversions

## Test
With the device listed from previous step, perform a quick recording to a file:<br/>
arecord -D plughw:CARD=U0x46d0x8ce,DEV=0 --duration=30 test.wav

