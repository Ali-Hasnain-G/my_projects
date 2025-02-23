from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response, current_app
import cv2
import numpy as np
import os
import joblib
import time
from datetime import datetime
import logging

app = Flask(__name__)

# Set up paths and configurations
app.config['UPLOAD_FOLDER'] = 'static/UPLOAD_FOLDER'
app.config['PROCESSED_FOLDER'] = 'static/PROCESSED_FOLDER'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Load the trained model
model = joblib.load('model.pkl')

# Disable caching for static files
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    # Add timestamp to bypass caching in the browser
    timestamp = datetime.now().timestamp()
    frame_path = os.path.join(app.config['PROCESSED_FOLDER'], 'frame.jpg')
    frame_available = os.path.exists(frame_path)
    return render_template('index.html', frame_available=frame_available, timestamp=timestamp)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        print("No video file part in request")
        return redirect(url_for('index'))
    
    video_file = request.files['video']
    if video_file.filename == '':
        print("No selected file")
        return redirect(url_for('index'))

    # Save the uploaded file
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'video.mp4')
    video_file.save(video_path)
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not saved correctly.")
        return redirect(url_for('index'))
    
    # Process the video
    start_time = time.time()
    process_video(video_path)
    end_time = time.time()
    
    processing_time = end_time - start_time
    print(f"Video processing completed in {processing_time:.2f} seconds.")
    
    return redirect(url_for('index'))

@app.route('/processed_frame')
def processed_frame():
    # Ensure the processed folder is correctly set
    processed_folder = app.config.get('PROCESSED_FOLDER', None)

    if not processed_folder:
        current_app.logger.error("Processed folder not configured.")
        return "Processed folder not configured", 500

    # Define the path to the processed frame
    frame_path = os.path.join(processed_folder, 'frame.jpg')

    # Check if the frame file exists
    if os.path.exists(frame_path):
        # Get the file modification time
        last_modified_time = os.path.getmtime(frame_path)
        last_modified = datetime.utcfromtimestamp(last_modified_time).strftime('%a, %d %b %Y %H:%M:%S GMT')

        # Check if the client sent the 'If-Modified-Since' header
        if 'If-Modified-Since' in request.headers:
            if_modified_since = request.headers.get('If-Modified-Since')

            # Compare the times to determine if the file has been modified
            if if_modified_since == last_modified:
                # Return a 304 Not Modified response
                return '', 304

        # Serve the processed frame with cache-busting headers
        response = make_response(send_from_directory(processed_folder, 'frame.jpg'))
        response.headers['Last-Modified'] = last_modified
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        # Return a 404 error if the frame file is not found
        current_app.logger.error(f"File not found at: {frame_path}")
        return "No processed frame available", 404
    
def process_video(video_path):
    print("Starting video processing...")
    cap = cv2.VideoCapture(video_path)
    tracker = cv2.TrackerCSRT_create()

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read video")
        cap.release()
        return

    # Manually select the bounding box (fixed box for demo purposes)
    bbox = (100, 100, 200, 200)
    tracker.init(frame, bbox)

    # Flag to check if the frame has been saved
    frame_saved = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Update the tracker and predict outcome
        success, bbox = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in bbox]
            ball_speed = np.random.uniform(0, 20)
            wheel_speed = np.random.uniform(0, 20)
            outcome = model.predict([[ball_speed, wheel_speed]])[0]

            # Draw bounding box and prediction on the frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f'Prediction: {outcome:.2f}', (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save the processed frame only once
        if not frame_saved:
            frame_path = os.path.join(app.config['PROCESSED_FOLDER'], 'frame.jpg')
            cv2.imwrite(frame_path, frame)
            print(f"Processed frame saved at {frame_path}.")
            frame_saved = True

    cap.release()
    cv2.destroyAllWindows()
    print("Video processing complete.")

if __name__ == '__main__':
    app.run(debug=True)
