from ultralytics import YOLO
import cv2
import socketio
import time
import cameraModule as cM

model = YOLO('yolov8n.pt')  # Load YOLOv8 Nano model

# Initialize the Socket.IO client
sio = socketio.Client()
server_url = "http://10.0.0.184:5000"

@sio.event
def connect():
    print("Connected to the server")

@sio.event
def disconnect():
    print("Disconnected from the server")

@sio.on('inference')
def handle_inference(data):
    print("Detections:", data)  # Print YOLO detections
    '''x1, y1, x2, y2 = map(int, data[0]['bbox'])  # YOLO outputs xyxy format
    label = data[0]['label']   # Get the class label
    confidence = data[0]['confidence']              # Get the confidence score
    
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
    )   '''

@sio.on('control')
def hanlde_control(data):
    print("Control Data: ", data)

# Connect to the server
sio.connect(server_url)

# Initialize the camera

fps_limit = 5  # Limit to 5 FPS
last_frame_time = 0

while True:
    frame = cM.getImgR(False, [680,440])

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