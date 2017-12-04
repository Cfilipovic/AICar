#!flask/bin/python
from flask import Flask
from bluepy import btle
import binascii

app = Flask(__name__)

global driveConfig

@app.route('/aicar/connect/', methods=['GET'])
def connect():
    dev=btle.Peripheral("1c:0f:ea:24:f1:4e")
    driveCmd=btle.UUID("0000ffe5-0000-1000-8000-00805f9b34fb")
    driveService=dev.getServiceByUUID(driveCmd)

    driveUuidConfig=btle.UUID("0000ffe9-0000-1000-8000-00805f9b34fb")
    global driveConfig
    driveConfig=driveService.getCharacteristics(driveUuidConfig)[0]
    return 200

@app.route('/aicar/forward/<string:speed>/<string:time>', methods=['GET'])
def forward(speed, time):
    driveConfig.write(bytes("\x71\x12\x54".format(speed, time)))
    return 200

@app.route('/aicar/turn-left/<string:angle>/<string:time>', methods=['GET'])
def turn_left(angle, time):
    driveConfig.write(bytes("\x73\x{}\xa{}".format(angle, time)))
    return 200

@app.route('/aicar/turn-right/<string:angle>/<string:time>', methods=['GET'])
def turn_right(angle, time):
    driveConfig.write(bytes("\x74\x{}\xa{}".format(angle, time)))
    return 200

if __name__ == '__main__':
    app.run()
