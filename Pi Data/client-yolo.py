from ultralytics import YOLO
from MotorModule import Motor
import cv2
import socketio
import time
import cameraModule as cM

##################################
###Define Motor Config###
# Pin Order for motor class connected to L298N board: EnA In1 In2 (left), EnB, In3, In4(right)
motor = Motor(2,3,4, 22,17,27)
##################################
control_data = None
#######
'''
Client collects frames from the front mounted cameras and sends those frames from the Raspberry Pi 
to the Flask server over socketio. The Client then awaits for a response from the server with the 'inference' 
data or 'control' inputs to the motors.
'''
#######

model = YOLO('yolov8n.pt')  # Load YOLOv8 Nano model

# Initialize the Socket.IO client
sio = socketio.Client()
server_url = "http://10.0.0.184:5000"

@sio.event
def connect():
    print("Connected to the server")
    emit_telemetry()

@sio.event
def disconnect():
    print("Disconnected from the server")

@sio.on('inference')
def handle_inference(data):
    pass#print("Detections:", data)  # Print YOLO detections

@sio.on('control')
def hanlde_control(data):
    #print("Control Data: ", data)
    global control_data
    control_data = data

def emit_telemetry():
    """Def"""
    fps_limit = 5  # Limit to 5 FPS
    last_frame_time = 0

    while True:
        frame = cM.getImgR(False, [680,440])
        global control_data

        if control_data is not None:
            print("Telemetry using control data:", control_data)
            if control_data['throttle'] == 0.0:
                print('stop')
                motor.stop()
            else:
                print('move')
                motor.move(control_data['throttle'],control_data['steerAngle'], control_data['time'])
        else:
            print("No control data received yet.")

        # Limit the frame rate
        current_time = time.time()
        if current_time - last_frame_time < 1 / fps_limit:
            continue
        last_frame_time = current_time

        # Encode frame as JPEG
        _, img_encoded = cv2.imencode('.jpg', frame)

        # Send the frame to the server
        sio.emit('frame', img_encoded.tobytes())

        # Display the frame locally
        cv2.imshow('Raspberry Pi Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    sio.disconnect()

# Connect to the server
sio.connect(server_url)
sio.wait()

