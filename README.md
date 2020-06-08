# DoorButler
Smart video doorbell<br/>

## Goals
Device should provide the following capabilities
- Smart voice screening<br/>
- Led status indicator<br/>
- MQTT<br/>
- Presence detection<br/>
Maybe:
- Video streaming<br/>
- REST api><br/>
- Two way audio<br/>

## Status
As June 2020, moved to Node-red using a RPI Zero W. It can play pre-recorded audio clips, then records few seconds of a response, and sends it to WIT.AI for language understanding. WIT.AI returns an intent that is processed by node-red.
It is triggered by mqtt start command.

## Reference (Credits)
https://github.com/alaudet/hcsr04sensor<br/>
https://github.com/eclipse/paho.mqtt.python<br/>
https://github.com/azlux/pymumble<br/>
https://bitbucket.org/mkuron/sip2mumble/overview
https://github.com/larsimmisch/pyalsaaudio<br/>
Motion <http://lavrsen.dk/foswiki/bin/view/Motion/WebHome><br/>
Mumble-server <http://wiki.mumble.info/wiki/Installing_Mumble><br/>
