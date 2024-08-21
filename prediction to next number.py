import cv2
import numpy as np
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

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
        self.root = root
        self.video_path = self.select_video_file()
        self.cap = cv2.VideoCapture(self.video_path)
        self.tracker = cv2.TrackerCSRT_create()
        self.model = PredictionModel()
        self.bbox = None

        # Create Tkinter canvas for displaying video frames
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()
        
        self.init_tracking()

    def select_video_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
        if not file_path:
            raise ValueError("No video file selected")
        return file_path

    def init_tracking(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to read video")
            self.cleanup()
            return
        
        # Allow user to manually select the bounding box
        self.bbox = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select ROI")
        
        if self.bbox != (0, 0, 0, 0):  # Ensure a valid ROI was selected
            self.tracker.init(frame, self.bbox)
        else:
            print("No bounding box selected. Exiting.")
            self.cleanup()

        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cleanup()
            return
        
        # Update the tracker
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

    def cleanup(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        cv2.destroyAllWindows()

# Run the application 
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Video Tracker")  # Set window title
    app = App(root)
    root.mainloop()
