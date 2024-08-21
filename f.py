from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
from sklearn.linear_model import LinearRegression
import tempfile
import os

app = Flask(__name__)

# Define the prediction model
class PredictionModel:
    def __init__(self):
        # Initialize model with example coefficients
        self.model = LinearRegression()
        self.model.coef_ = np.array([0.5, 0.3])
        self.model.intercept_ = 0.0

    def predict(self, ball_speed, wheel_speed):
        return self.model.predict(np.array([[ball_speed, wheel_speed]]))[0]

# Initialize the prediction model
model = PredictionModel()

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    video_file = request.files['video']
    
    if video_file.filename == '':
        return jsonify({'error': 'No selected video file'}), 400
    
    # Save the uploaded video file to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    video_file.save(temp_file.name)
    video_path = temp_file.name

    # Process video
    results = process_video(video_path)

    # Clean up temporary file
    os.remove(temp_file.name)

    return jsonify(results)

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    tracker = cv2.TrackerCSRT_create()
    bbox = None
    results = []

    # Read the first frame and initialize the tracker
    ret, frame = cap.read()
    if not ret:
        return {'error': 'Failed to read video'}

    # Initialize tracker with a default bounding box
    bbox = (100, 100, 200, 200)  # Placeholder for default bounding box
    tracker.init(frame, bbox)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Update the tracker
        success, bbox = tracker.update(frame)
        
        if success:
            (x, y, w, h) = [int(v) for v in bbox]
            ball_speed = np.random.uniform(0, 20)  # Simulated ball speed
            wheel_speed = np.random.uniform(0, 20)  # Simulated wheel speed
            outcome = model.predict(ball_speed, wheel_speed)
            
            # Store results
            results.append({
                'bbox': [x, y, w, h],
                'ball_speed': ball_speed,
                'wheel_speed': wheel_speed,
                'prediction': outcome
            })
    
    cap.release()
    
    return {'frames': results}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    ball_speed = data.get('ball_speed', 0)
    wheel_speed = data.get('wheel_speed', 0)
    
    outcome = model.predict(ball_speed, wheel_speed)
    
    return jsonify({'prediction': outcome})

if __name__ == "__main__":
    app.run(debug=True)
