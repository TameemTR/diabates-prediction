# utils/preprocess.py

import numpy as np
import joblib

# Load the saved LabelEncoders
le_gender = joblib.load("model/le_gender.pkl")
le_location = joblib.load("model/le_location.pkl")
le_smoking = joblib.load("model/le_smoking.pkl")

# Load scaler
scaler = joblib.load("model/standard_scaler.pkl")

def transform_input(features: dict) -> np.ndarray:
    # Encode
    gender_encoded = le_gender.transform([features["gender"]])[0]
    location_encoded = le_location.transform([features["location"]])[0]
    smoking_encoded = le_smoking.transform([features["smoking_history"]])[0]

    x_raw = np.array([[
        features["age"],
        features["race:AfricanAmerican"],
        features["race:Asian"],
        features["race:Caucasian"],
        features["race:Hispanic"],
        features["race:Other"],
        features["hypertension"],
        features["heart_disease"],
        features["bmi"],
        features["hbA1c_level"],
        features["blood_glucose_level"],
        gender_encoded,
        location_encoded,
        smoking_encoded,
        0
    ]])

    x_scaled = scaler.transform(x_raw)

    print("Scaled input to model:", x_scaled)
    return x_scaled