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
Confirm your HW is listed
```
aplay -L
arecord -L
```
Test speakers
```
speaker-test
```
