import pymumble.pymumble_py3 as pymumble
import time

client = pymumble.Mumble("192.168.101.112", "doorBot", 64738, "2putipus", None, None, True, [], False)
client.set_codec_profile("audio")
client.start()
client.is_ready()

time.sleep(30)

