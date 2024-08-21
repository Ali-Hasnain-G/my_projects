import numpy as np
from sklearn.linear_model import LinearRegression

class PredictionModel:
    def __init__(self):
        # Initialize model with example coefficients
        self.model = LinearRegression()
        # Manually set coefficients and intercept
        self.model.coef_ = np.array([0.5, 0.3])
        self.model.intercept_ = 0.0

    def predict(self, ball_speed, wheel_speed):
        # Predict based on the input features
        return self.model.predict(np.array([[ball_speed, wheel_speed]]))[0]
