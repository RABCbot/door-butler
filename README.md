# Door Butler
Interactive voice assistant that helps identifies who is at the door and route visitors<br/>
## Goals
Wish list of capabilities:
* Smart voice screening (done)<br/>
* Dialog management (done)<br/>
* Led status indicator (done)<br/>
* Prerecorded answers (done)<br/>
* MQTT (done)<br/>
* Integration with Home-assistant (done)<br/>
* Video streaming<br/>
* Presence detection<br/>
* REST API<br/>
* Two-way audio<br/>
## Hardware
* Raspberry Pi Zero W<br/>
* Google AIY voice hat<br/>
* PlayStation Eye <br/>
## Software
* [WIT.AI](https://wit.ai/)
* Node-red 
![Flow](node-red/butler-flow.png)
## Installation
1. Install [Raspberry Pi OS](https://www.raspberrypi.org/downloads/) to an SD card
2. Install [Node-Red](https://nodered.org/docs/getting-started/raspberrypi)
3. Navigate to http://hostname:1880 and import the [DoorButler flow](https://github.com/RABCbot/door-butler/blob/master/node-red/butler-flow.json)
4. Create an [app](https://wit.ai/docs/quickstart) with wit.ai

