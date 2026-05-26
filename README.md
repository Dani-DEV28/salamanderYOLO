# 🦎 Salamander Finder

# Run instructions

1. Open PowerShell terminal in admin mode (run ```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```)
1. Run ```winget install ffmpeg``` to install ffmpeg 
1. Navigate to backend folder (```cd backend```)
1. Run ```python -m venv venv```
1. Run ```.\venv\scripts\activate```
1. Run ```pip install -r .\requirements.txt``` 
1. run ```main.py`
1. In new terminal run ```npm i```
1. Run ```npm run dev``` 

# Dataset Details
Used the YOLO bounding boxes to train model. 50 epochs with 8 batches. 

# Comparison
When comparing the YOLO model to contrast-based detection methods, YOLO is generally preferred in less controlled environments because it can detect and classify objects under varying conditions such as changes in lighting, background, and object positioning. In contrast, contrast-based detection performs better in ideal or controlled settings where the target object is clearly distinguishable from the background, making it a more reliable choice in those situations. Additionally, contrast-based detection allows for some flexibility in prioritizing or targeting the largest object within an image. While YOLO offers faster and more advanced object detection capabilities, it requires a significant amount of training data and model tuning to achieve high accuracy; otherwise, its performance may still have room for improvement.