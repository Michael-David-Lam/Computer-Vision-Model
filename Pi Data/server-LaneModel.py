import argparse
import base64
from datetime import datetime
import os
import shutil
import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO
from keras.models import load_model
import utils


# Initialize our socketio server
sio = socketio.Server()
app = Flask(__name__)

model = None

# For car speed
MAX_SPEED = 25
MIN_SPEED = 10
speed_limit = MAX_SPEED

# This event comes from the simulator many times per second along with the car data.
# We process the data and calculate some control values and then send them back to the simulator to drive the car.
@sio.on('telemetry')
def telemetry(sid, data):
    print("Received data from the simulator.")

    if not data:
        return sio.emit('manual', data={}, skip_sid=True)

    try:
        #speed = float(data["speed"]) # we can use this to speed up or down depending on the speed limit or signs and objects detected

        # We used 3 images for training (left, center, right), but here we only predict with the center camera.
        image = Image.open(BytesIO(base64.b64decode(data["image"])))

        image = np.asarray(image)       # from PIL image to numpy array
        image = utils.preprocess(image) # apply the preprocessing
        image = np.array([image])       # the model expects 4D array

        # Predicting the steering angle for the current center image
        steering_angle = float(model.predict(image, batch_size=1))

        # lower the throttle as the speed increases
        # if the speed is above the current speed limit, we are on a downhill.
        # make sure we slow down first and then go back to the original max speed.
        '''global speed_limit
        if speed > speed_limit:
            speed_limit = MIN_SPEED  # slow down
        else:
            speed_limit = MAX_SPEED
        throttle = 1.0 - steering_angle**2 - (speed/speed_limit)**2
        '''
        print(f"Sending the calculated steering angle ({steering_angle})") #and throttle({throttle}) to the simulation...")
        send_control(steering_angle)#, throttle)
    except Exception as e:
        print(e)


# A connect event that if we get means that the simulator is successfully connected to this python app.
@sio.on('connect')
def connect(sid, environ):
    print("Connected to the simulator.")
    send_control(0, 0)

# This function sends control data (steering angle & throttle) to the simulator. The car will be driven depending on these values.
def send_control(steering_angle):#, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__()
            #,'throttle': throttle.__str__()
        },
        skip_sid=True)


if __name__ == '__main__':
    model = load_model("./model-007.h5", compile=False)

    # Start the socketio server
    #eventlet.wsgi.server(eventlet.listen(('', 4567)), socketio.Middleware(sio, app))
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
