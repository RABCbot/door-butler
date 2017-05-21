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

In my case, I get a list of all devices, with the USB Microphone listed as:<br/>
null<br/>
    Discard all samples (playback) or generate zero samples (capture)<br/>
default:CARD=U0x46d0x8ce<br/>
    USB Device 0x46d:0x8ce, USB Audio<br/>
    Default Audio Device<br/>
hw:CARD=U0x46d0x8ce,DEV=0<br/>
    USB Device 0x46d:0x8ce, USB Audio<br/>
    Direct hardware device without any conversions<br/>

Find card index:<br/>
cat /proc/asound/modules<br/>
 0 snd_bcm2835<br/>
 1 snd_usb_audio<br/>

## Test
With the device listed from previous step, perform a quick recording to a file:<br/>
arecord -D plughw:CARD=U0x46d0x8ce,DEV=0 --duration=30 test.wav<br/>

## Reference
https://bitbucket.org/mkuron/sip2mumble/overview

