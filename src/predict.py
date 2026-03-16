import joblib
import numpy as np

model = joblib.load("models/model.pkl")

data = np.array([[80,120,40,15,2]])

prediction = model.predict(data)

print("Predicted AQI:", prediction)