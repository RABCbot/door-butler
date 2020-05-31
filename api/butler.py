import shlex
import subprocess
import logging
import json
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(filename="butler.log",level=logging.DEBUG)

ok = {"status": "ok"}
last_response = None

@app.route("/api/status", methods=["GET"])
def status():
  return json.dumps(ok)

@app.route("/api/response", methods=["GET"])
def response():
  return json.dumps(last_response)


@app.route("/api/run", methods=["POST"])
def command():
  global last_response
  _response = ok
  status = 200

  try:
    data = request.json
    for cmd in data["commands"]:
      logging.debug(cmd)
      cp = subprocess.run(cmd["args"], shell=True, timeout=60, capture_output=True)
      str = cp.stdout.decode("ascii")
      logging.debug(str)
      if "stdout" in cmd:
        _response = {"response":json.loads(str)}
        if "payload" in cmd:
          _response["payload"] = cmd["payload"]
        last_response = _response
  except Exception as ex:
    _response = {"args":cmd["args"], "exception":str(ex)}
    status = 500
    logging.error(ex)
  return json.dumps(_response), status

if __name__ == "__main__":
  app.debug = True
  app.run(host="0.0.0.0", port=8080)

