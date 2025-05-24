import joblib
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)

# Allow all CORS
CORS(app)

# Charger les modèles
clf_diagnostic = joblib.load("modele_diagnostic.pkl")
clf_disease = joblib.load("modele_maladie.pkl")

# Load disease mapping from diseases.txt
with open("diseases.txt", "r") as f:
    disease_list = [line.strip() for line in f.readlines()]

disease_mapping = {i: disease for i, disease in enumerate(disease_list)}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Convert input strings to the format expected by the model
    binary_cols = ["Fever", "Cough", "Fatigue", "Difficulty Breathing"]
    for col in binary_cols:
        data[col] = 1 if data[col] == "Yes" else 0

    categorical_mapping = {
        "Gender": {"Male": 0, "Female": 1},
        "Blood Pressure": {"Low": [1, 0], "Normal": [0, 1], "High": [0, 0]},
        "Cholesterol Level": {"Low": [1, 0], "Normal": [0, 1], "High": [0, 0]}
    }

    # Handle categorical features with one-hot encoding
    blood_pressure_encoded = categorical_mapping["Blood Pressure"][data["Blood Pressure"]]
    cholesterol_encoded = categorical_mapping["Cholesterol Level"][data["Cholesterol Level"]]

    # Ensure Gender is encoded correctly
    data["Gender"] = categorical_mapping["Gender"][data["Gender"]]

    # Create a DataFrame with the correct feature names for modele_diagnostic.pkl
    diagnostic_input_data = {
        "Disease": 0,
        "Fever": data["Fever"],
        "Cough": data["Cough"],
        "Fatigue": data["Fatigue"],
        "Difficulty Breathing": data["Difficulty Breathing"],
        "Age": int(data["Age"]),
        "Gender": data["Gender"],
        "Blood Pressure_Low": blood_pressure_encoded[0],
        "Blood Pressure_Normal": blood_pressure_encoded[1],
        "Cholesterol Level_Low": cholesterol_encoded[0],
        "Cholesterol Level_Normal": cholesterol_encoded[1]
    }

    diagnostic_input_df = pd.DataFrame([diagnostic_input_data])

    # Create a DataFrame with the correct feature names for modele_maladie.pkl
    disease_input_data = {
        "Fever": data["Fever"],
        "Cough": data["Cough"],
        "Fatigue": data["Fatigue"],
        "Difficulty Breathing": data["Difficulty Breathing"],
        "Age": int(data["Age"]),
        "Gender": data["Gender"],
        "Outcome Variable": 0,
        "Blood Pressure_Low": blood_pressure_encoded[0],
        "Blood Pressure_Normal": blood_pressure_encoded[1],
        "Cholesterol Level_Low": cholesterol_encoded[0],
        "Cholesterol Level_Normal": cholesterol_encoded[1]
    }

    disease_input_df = pd.DataFrame([disease_input_data])

    # Make predictions
    prediction_disease = clf_disease.predict(disease_input_df)[0]
    prediction_diagnostic = clf_diagnostic.predict(diagnostic_input_df)[0]

    # Decode predictions back to human-readable format
    diagnostic_mapping = {0: "Negative", 1: "Positive"}

    # Validate predictions
    disease_label = disease_mapping.get(prediction_disease, f"Unknown Class {prediction_disease}")
    diagnostic_label = diagnostic_mapping.get(prediction_diagnostic, f"Unknown Class {prediction_diagnostic}")

    return jsonify({
        "disease_prediction": disease_label,
        "diagnostic_prediction": diagnostic_label
    })

if __name__ == "__main__":
    app.run(debug=True)
