import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
df = pd.read_csv("data/Delhi_AQI_Dataset.csv")

# Select features
X = df[['PM2.5','PM10','NO2','SO2','CO']]

# Target
y = df['AQI']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# Model
model = RandomForestRegressor()

# Train model
model.fit(X_train,y_train)

# Save model
joblib.dump(model,"models/model.pkl")

print("Model saved successfully")