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
- REST API<br/>
- Two way audio<br/>

## Status
As June 2020, moved to Node-red using a RPI Zero W. It can play pre-recorded audio clips, then records few seconds of a response, and sends it to WIT.AI for language understanding. WIT.AI returns an intent that is processed by node-red.</br>
Supports a basic copy of hermes mqtt protocol, to start process (instead of a wake word) and send intents
