# utils/predict.py

import numpy as np
from tensorflow.keras.models import load_model
from utils.preprocess import transform_input

# Load your trained model
model = load_model("model/diabetes_model_v3.h5")

def predict_diabetes(features: dict) -> int:
    """
    Predicts diabetes risk using 15 input features.
    Returns 1 if high risk, 0 otherwise.
    """

    # Preprocess and encode input
    x = transform_input(features)

    print("Final input to model:", x)


    # Predict using the neural network
    prediction = model.predict(x)[0][0]
    
    # Debug output in terminal
    print("Encoded + transformed input prediction:", prediction)

    # Return binary classification
    return int(prediction >= 0.5)

    print("Model loaded:", model.name)
    model.summary()
