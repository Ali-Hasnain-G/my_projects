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
        self.tracker_ball = cv2.TrackerCSRT_create()
        self.tracker_wheel = cv2.TrackerCSRT_create()
        self.model = PredictionModel()
        self.bbox_ball = None
        self.bbox_wheel = None
        self.previous_positions_ball = None
        self.previous_positions_wheel = None
        self.ball_speed = 0.0
        self.wheel_speed = 0.0

        # Create Tkinter canvas and UI elements
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.ball_speed_label = tk.Label(root, text="Ball Speed:")
        self.ball_speed_label.pack()
        self.ball_speed_value = tk.Label(root, text="0.0")
        self.ball_speed_value.pack()

        self.wheel_speed_label = tk.Label(root, text="Wheel Speed:")
        self.wheel_speed_label.pack()
        self.wheel_speed_value = tk.Label(root, text="0.0")
        self.wheel_speed_value.pack()

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
        
        # Allow user to manually select the bounding boxes
        self.bbox_ball = cv2.selectROI("Select Ball ROI", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select Ball ROI")
        
        self.bbox_wheel = cv2.selectROI("Select Wheel ROI", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select Wheel ROI")
        
        if self.bbox_ball != (0, 0, 0, 0):  # Ensure a valid ROI was selected for the ball
            self.tracker_ball.init(frame, self.bbox_ball)
        
        if self.bbox_wheel != (0, 0, 0, 0):  # Ensure a valid ROI was selected for the wheel
            self.tracker_wheel.init(frame, self.bbox_wheel)

        self.previous_positions_ball = [self.bbox_ball[:2]]
        self.previous_positions_wheel = [self.bbox_wheel[:2]]

        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cleanup()
            return
        
        # Update the trackers
        success_ball, bbox_ball = self.tracker_ball.update(frame)
        success_wheel, bbox_wheel = self.tracker_wheel.update(frame)
        
        if success_ball:
            (x_ball, y_ball, w_ball, h_ball) = [int(v) for v in bbox_ball]
            current_position_ball = (x_ball + w_ball / 2, y_ball + h_ball / 2)
            self.previous_positions_ball.append(current_position_ball)
            
            if len(self.previous_positions_ball) > 2:
                speed_x = self.previous_positions_ball[-1][0] - self.previous_positions_ball[-2][0]
                speed_y = self.previous_positions_ball[-1][1] - self.previous_positions_ball[-2][1]
                self.ball_speed = np.sqrt(speed_x**2 + speed_y**2)

            # Draw ball bounding box and speed
            cv2.rectangle(frame, (x_ball, y_ball), (x_ball + w_ball, y_ball + h_ball), (255, 0, 0), 2)
            cv2.putText(frame, f'Ball Speed: {self.ball_speed:.2f}', (x_ball, y_ball - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        if success_wheel:
            (x_wheel, y_wheel, w_wheel, h_wheel) = [int(v) for v in bbox_wheel]
            current_position_wheel = (x_wheel + w_wheel / 2, y_wheel + h_wheel / 2)
            self.previous_positions_wheel.append(current_position_wheel)
            
            if len(self.previous_positions_wheel) > 2:
                speed_x = self.previous_positions_wheel[-1][0] - self.previous_positions_wheel[-2][0]
                speed_y = self.previous_positions_wheel[-1][1] - self.previous_positions_wheel[-2][1]
                self.wheel_speed = np.sqrt(speed_x**2 + speed_y**2)

            # Draw wheel bounding box and speed
            cv2.rectangle(frame, (x_wheel, y_wheel), (x_wheel + w_wheel, y_wheel + h_wheel), (0, 255, 0), 2)
            cv2.putText(frame, f'Wheel Speed: {self.wheel_speed:.2f}', (x_wheel, y_wheel - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Update speeds in the UI
        self.ball_speed_value.config(text=f"{self.ball_speed:.2f}")
        self.wheel_speed_value.config(text=f"{self.wheel_speed:.2f}")

        # Calculate prediction
        outcome = self.model.predict(self.ball_speed, self.wheel_speed)
        cv2.putText(frame, f'Prediction: {outcome:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

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
