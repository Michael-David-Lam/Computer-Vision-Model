import socketio
import random
import time

from MotorModule import Motor
import cv2
import cameraModule as cM

'''
How the client should interact with the lane detection/deep learning model
'''

##################################
###Define Motor Config###
# Pin Order for motor class connected to L298N board: EnA In1 In2 (left), EnB, In3, In4(right)
motor = Motor(2,3,4, 22,17,27)
##################################
steer_data = None

# Initialize the Socket.IO client
sio = socketio.Client()
server_url = "http://10.0.0.184:5000"

# This will run when we are connected to the server
@sio.event
def connect():
    print('Connected to the server')
    # Start emitting telemetry data
    emit_telemetry()

@sio.event
def disconnect():
    print("Disconnected from the server")

# Here we are getting the calculated steering angle value with AI
@sio.on('steer')
def on_steer(data):
    global steer_data
    steer_data = data['steering_angle']
    print('Got steering data:', data)

# Emit telemetry data 5 times per second. Here we are sending the car data to the server to then calculate a steering angle for us.
def emit_telemetry():
    fps_limit = 5  # Limit to 5 FPS
    last_frame_time = 0
    while True:

        frame = cM.getImgR(False, [680,440])
        global steer_data

        if steer_data is not None:
            print("Telemetry using control data:", steer_data)
            motor.move(0.3, steer_data, 0.1)

        else:
            print("No control data received yet.")

        current_time = time.time()
        if current_time - last_frame_time < 1 / fps_limit:
            continue
        last_frame_time = current_time
        
        # Encode frame as JPEG
        _, img_encoded = cv2.imencode('.jpg', frame)

        # Simulating telemetry data
        telemetry_data = {
            'image': img_encoded,  # sending a random speed
            # In the real Unity simulator, the images from 3 cameras should also be sent
        }
        # Send the frame to the server
        sio.emit('telemetry', img_encoded.tobytes())
        print('Emitting telemetry data:', telemetry_data)


        # Display the frame locally
        cv2.imshow('Raspberry Pi Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Wait for 0.2 seconds (or as needed)
        time.sleep(0.2)
    cv2.destroyAllWindows()
    sio.disconnect()

# Connect to the server
sio.connect(server_url)
sio.wait()
