# project to do prediction according to the speed of ball and wheel

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

# creatoin of own dataset of values
# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic data
num_samples = 100
ball_speed = np.random.uniform(0, 20, num_samples)  # Ball speeds between 0 and 20 m/s
wheel_speed = np.random.uniform(0, 20, num_samples)  # Wheel speeds between 0 and 20 m/s
target_variable = 0.5 * ball_speed + 0.3 * wheel_speed + np.random.normal(0, 1, num_samples)  # Example target

# Create a DataFrame
data = pd.DataFrame({
    'ball_speed': ball_speed,
    'wheel_speed': wheel_speed,
    'target_variable': target_variable
})

# Save to CSV
data.to_csv('ball_wheel_data.csv', index=False)

print("Dataset created and saved as 'ball_wheel_data.csv'.")

# Load data
data = pd.read_csv('ball_wheel_data.csv')

# Prepare features and target variable
X = data[['ball_speed', 'wheel_speed']]
y = data['target_variable']  # e.g., distance traveled

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the model
joblib.dump(model, 'ball_wheel_model.pkl')

# Load and use the model
model = joblib.load('ball_wheel_model.pkl')
new_data = pd.DataFrame({'ball_speed': [10], 'wheel_speed': [5]})
prediction = model.predict(new_data)
print(f"Prediction: {prediction}")
