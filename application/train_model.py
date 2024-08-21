import numpy as np
import joblib
from sklearn.linear_model import LinearRegression

# Generate some example data
X = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]])
y = np.array([2, 4, 6, 8, 10])

# Train a LinearRegression model
model = LinearRegression()
model.fit(X, y)

# Save the trained model to a file
joblib.dump(model, 'model.pkl')

print("Model saved to 'model.pkl'")
