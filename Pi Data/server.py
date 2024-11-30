from ultralytics import YOLO
import cv2 
import numpy as np
from time import sleep

import socketio 
from flask import Flask

# Create Flask and Socket.IO server
app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins="*")  # Enable CORS for cross-origin requests
model = YOLO('yolov8n.pt')  # Load YOLOv8 Nano model

# Wrap the Flask app with the Socket.IO app
app = socketio.WSGIApp(sio, app)

@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on('frame')
def handle_frame(sid, data):
    # Decode the image from bytes
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform YOLO inference
    results = model(img)
    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                'label': model.names[int(box.cls)],
                'confidence': float(box.conf),
                'bbox': box.xyxy.tolist()
            })

    '''if detections['label'] == '20KPH':
        #steering_angle=0
        throttle = 0.2
    '''
    # Send detections back to the client
    sio.emit('inference', detections, to=sid)
    #send_control(throttle)

def send_control(throttle):
    sio.emit(
        "inference",
        data={
            'throttle': throttle.__str__()
        },
        skip_sid=True)

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)