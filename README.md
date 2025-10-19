# Computer Vision Project - Autonomous Raspberry Pi Robot 🚗🔍

This project houses a complete computer vision project for an autonomous robot car powered by a Raspberry Pi and webcam.  
The system is designed to detect road signs in real time and make navigation decisions using a trained YOLO model.  

### How it works:
- A **Raspberry Pi robot car** captures video through an onboard webcam.  
- A **YOLO model**, trained on road sign data, runs on a local server to perform inference.  
- The server communicates results to the Pi via **WebSocket**.  
- The **Raspberry Pi processes the detections** and adjusts the robot car’s throttle to react to road signs.  
   
****
