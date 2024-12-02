import socketio
import random
import time

'''
How the client should interact with the lane detection/deep learning model
'''

# Connect to the server
sio = socketio.Client()

# This will run when we are connected to the server
@sio.event
def connect():
    print('Connected to Python server')

    # Start emitting telemetry data
    emit_telemetry()

# Here we are getting the calculated steering angle value with AI
@sio.on('steer')
def on_steer(data):
    print('Got steering data:', data)

# When we disconnect from the server
@sio.event
def disconnect():
    print('Disconnected from the server')

# Emit telemetry data 5 times per second. Here we are sending the car data to the server to then calculate a steering angle for us.
def emit_telemetry():
    while True:
        # Simulating telemetry data
        telemetry_data = {
            'speed': round(random.uniform(0, 100), 2),  # sending a random speed
            # In the real Unity simulator, the images from 3 cameras should also be sent
        }

        print('Emitting telemetry data:', telemetry_data)

        # Send telemetry event to the server
        sio.emit('telemetry', telemetry_data)

        # Wait for 0.2 seconds (or as needed)
        time.sleep(0.2)

# Connect to the server
sio.connect('http://localhost:4567')
sio.wait()