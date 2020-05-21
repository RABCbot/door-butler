Taken from https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-wiring

## Wiring
Amp Vin to Raspbery Pi 5V #4<br/>
Amp GND to Raspbery Pi GND #6<br/>
Amp DIN to Raspbery Pi Pin #21<br/>
Amp BCLK to Raspbery Pi Pin #18<br/>
Amp LRCLK to Raspbery Pi Pin #19<br/>

## Installation

Using Adafruit script
curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash

Details from Adafruit:<br/>
sudo nano /etc/asound.conf
```
pcm.speakerbonnet {
   type hw card 0
}

pcm.dmixer {
   type dmix
   ipc_key 1024
   ipc_perm 0666
   slave {
     pcm "speakerbonnet"
     period_time 0
     period_size 1024
     buffer_size 8192
     rate 44100
     channels 2
   }
}

ctl.dmixer {
    type hw card 0
}

pcm.softvol {
    type softvol
    slave.pcm "dmixer"
    control.name "PCM"
    control.card 0
}

ctl.softvol {
    type hw card 0
}

pcm.!default {
    type             plug
    slave.pcm       "softvol"
}
```

sudo nano /boot/config.txt<br/>
```
#dtparam=audio=on
dtoverlay=hifiberry-dac
dtoverlay=i2s-mmap
```
