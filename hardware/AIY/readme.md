Create asound.conf
```
sudo nano /etc/asound.conf
```
Paste text below:
```
pcm.softvol {
    type softvol
    slave.pcm dmix
    control {
        name Master
        card 0
    }
}

pcm.micboost {
    type route
    slave.pcm dsnoop
    ttable {
        0.0 30.0
        1.1 30.0
    }
}

pcm.!default {
    type asym
    playback.pcm "plug:softvol"
    capture.pcm "plug:micboost"
}

ctl.!default {
    type hw
    card 0
}
```
repeat for ~/.asoundrc</br>

Edit config.txt
```
sudo nano /boot/config.txt
```
Scroll to bottom and edit/add text as shown:
```
#dtparam=audio=on
dtoverlay=i2s-mmap
dtoverlay=googlevoicehat-soundcard
```
Reboot</br>
Confirm your HW is listed
```
aplay -L
arecord -L
```
Test speakers
```
speaker-test -t wav
```

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

With the device listed from previous step, perform a quick recording to a file:<br/>
arecord -D plughw:CARD=U0x46d0x8ce,DEV=0 --duration=30 test.wav<br/>

Change volume
amixer sset PCM,0 90%


