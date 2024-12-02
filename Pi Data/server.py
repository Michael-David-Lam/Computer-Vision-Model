from ultralytics import YOLO
import cv2 
import numpy as np
from time import sleep

import socketio 
from flask import Flask

#######
'''
Server handles incoming frames from the Raspberry Pi and send 'Detection' and 'Control events back to the Pi based on
the information predicted by the YOLO model 
'''
#######

# Create Flask and Socket.IO server
app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins="*")  # Enable CORS for cross-origin requests
model = YOLO('roadsigns_yolo_v2.pt')  # Load YOLOv8 Nano model

# Wrap the Flask app with the Socket.IO app
app = socketio.WSGIApp(sio, app)

@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    #cv2.destroyAllWindows()      
    print(f"Client disconnected: {sid}")
    # Close cv windows on client disconnect
    

@sio.on('frame')
def handle_frame(sid, data):
    # Decode the image from bytes
    nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    current_label = None

    # Perform YOLO inference
    predict = model(frame, conf=0.5)
    detections = []
    for result in predict:
        for box in result.boxes:
            detections.append({
                'label': model.names[int(box.cls)],
                'confidence': float(box.conf),
                'bbox': box.xyxy.tolist()
            })

            x1, y1, x2, y2 = map(int, box.xyxy[0])  # YOLO outputs xyxy format
            label = model.names[int(box.cls[0])]   # Get the class label
            confidence = box.conf[0]              # Get the confidence score
            
            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{label} {confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )   
            if current_label is None:
                current_label = label
    '''if current_label == 'person':
        
        send_control(0.5, 0.0, 0.5)
    else:
        send_control(0.0, 0.0, 0.0)
    '''    
    # Display the frame
    cv2.imshow("Detections", frame)
   
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()      

    
    # Send detections back to the client
    sio.emit('inference', detections, to=sid)


def send_control(throttle, steerAngle, time):
    sio.emit(
        "control",
        data={
            'throttle': throttle,
            'steerAngle': steerAngle,
            'time': time
        },
        skip_sid=True)

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)