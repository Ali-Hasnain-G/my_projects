import cv2
import numpy as np
from sklearn.linear_model import LinearRegression
import tkinter as tk
from PIL import Image, ImageTk
from pytube import YouTube
import os

# Define the prediction model
class PredictionModel:
    def __init__(self):
        # Initialize model with example coefficients
        self.model = LinearRegression()
        self.model.coef_ = np.array([0.5, 0.3])
        self.model.intercept_ = 0.0

    def predict(self, ball_speed, wheel_speed):
        return self.model.predict(np.array([[ball_speed, wheel_speed]]))[0]

# Initialize video upload
class App:
    def __init__(self, root):
        self.video_url = 'https://www.youtube.com/watch?v=MD3nuLMPzyg'  # Replace with your YouTube URL
        self.video_path = None
        
        try:
            self.video_path = self.download_video(self.video_url)
            self.cap = cv2.VideoCapture(self.video_path)
            self.tracker = cv2.TrackerCSRT_create()
            self.init_tracking()
        except Exception as e:
            print(f"Error initializing application: {e}")
            self.cleanup()

    def download_video(self, url):
        try:
            yt = YouTube(url)
            yt.check_availability()  # Check if the video is available
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            if stream is None:
                raise ValueError("No suitable streams found for the video.")
            video_path = stream.download(filename='downloaded_video.mp4')
            return video_path
        except Exception as e:
            print(f"Error downloading video: {e}")
            raise  # Re-raise the exception to be caught by the caller

    def init_tracking(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to read video")
            self.cleanup()
            return
        
        # Define an initial bounding box
        bbox = (100, 100, 200, 200)  # Example bounding box coordinates
        self.tracker.init(frame, bbox)

    def process_video(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Update the tracker
            success, bbox = self.tracker.update(frame)
            
            # Draw the bounding box
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        if hasattr(self, 'video_path') and os.path.exists(self.video_path):
            os.remove(self.video_path)
        cv2.destroyAllWindows()
        
        # Initialize the first frame for tracking
        ret, frame = self.vid.read()
        if ret:
            self.bbox = cv2.selectROI(frame, False)
            self.tracker.init(frame, self.bbox)
        
        self.update()
        self.root.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            success, bbox = self.tracker.update(frame)
            
            if success:
                (x, y, w, h) = [int(v) for v in bbox]
                ball_speed = np.random.uniform(0, 20)  # Simulated ball speed
                wheel_speed = np.random.uniform(0, 20)  # Simulated wheel speed
                outcome = self.model.predict(ball_speed, wheel_speed)
                
                # Draw bounding box and prediction
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, f'Prediction: {outcome:.2f}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Convert frame to Image for Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        self.root.after(10, self.update)

        def __del__(self):
         if hasattr(self, 'cap'):
            self.cap.release()
        cv2.destroyAllWindows()

# Run the application 
if __name__ == "__main__":
    root = None  # Replace with actual root if necessary
    app = App(root)
    if app.video_path:
        app.process_video()