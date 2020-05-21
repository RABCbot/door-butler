import re
import subprocess
import logging
import json
from flask import Flask, request


app = Flask(__name__)
logging.basicConfig(filename="butler.log",level=logging.DEBUG)

ok = {"status": "ok"}

@app.route("/api/status", methods=["GET"])
def status():
  return json.dumps(ok)


@app.route("/api/run", methods=["POST"])
def command():
  msg = ok
  status = 200
  try:
    data = request.json
    for cmd in data["commands"]:
      args = cmd["args"]
      subprocess.check_call(args.split(" "), timeout=60)
      logging.debug(args)
  except Exception as ex:
    msg = {"status": "exception", "message":str(ex)}
    status = 500
    logging.error(ex)
  return json.dumps(msg), status

if __name__ == "__main__":
  app.debug = True
  app.run(host="0.0.0.0", port=8080)
