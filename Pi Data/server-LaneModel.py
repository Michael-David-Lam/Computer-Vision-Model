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
import cv2


# Initialize our socketio server
app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins="*")

# Wrap the Flask app with the Socket.IO app
app = socketio.WSGIApp(sio, app)

model = None

# For car speed
MAX_SPEED = 25
MIN_SPEED = 10
speed_limit = MAX_SPEED


# A connect event that if we get means that the simulator is successfully connected to this python app.
@sio.event
def connect(sid, environ):
    print("Connected to the Pi.")
    send_control(0)

@sio.event
def disconnect(sid):
    #cv2.destroyAllWindows()      
    print(f"Client disconnected: {sid}")
    # Close cv windows on client disconnect

# This event comes from the simulator many times per second along with the car data.
# We process the data and calculate some control values and then send them back to the simulator to drive the car.
@sio.on('telemetry')
def telemetry(sid, data):
    print("Received data from the simulator.")

    if not data:
        return sio.emit('manual', data={}, skip_sid=True)

    try:
        # We used 3 images for training (left, center, right), but here we only predict with the center camera.
        nparr = np.frombuffer(data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = np.asarray(image)       # from PIL image to numpy array
        image = utils.preprocess(image) # apply the preprocessing
        image = np.array([image])       # the model expects 4D array

        # Predicting the steering angle for the current center image
        steering_angle = float(model.predict(image, batch_size=1))

        print(f"Sending the calculated steering angle ({steering_angle})")

        # Send angle to client
        send_control(steering_angle) 
    except Exception as e:
        print(e)



# This function sends control data, the car will be driven depending on these values.
def send_control(steering_angle): 
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle
            #,'throttle': throttle.__str__()
        },
        skip_sid=True)


if __name__ == '__main__':
    model = load_model("./model-007.h5", compile=False)

    # Start the socketio server
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
