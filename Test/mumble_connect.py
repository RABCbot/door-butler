import pymumble.pymumble_py3 as pymumble
import time

client = pymumble.Mumble("your mumble server", "DoorButler", 64738, "your mumble password", None, None, True, [], False)
client.set_codec_profile("audio")
client.start()
client.is_ready()

time.sleep(30)

