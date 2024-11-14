import numpy as np
import joblib

# -- Loading the trained model --
model = joblib.load("./finModel.joblib")

def calculate_risk_score(inputs):
    expected_features = model.n_features_in_
    print(f"Number of features expected by the model: {expected_features}")
    
    input_data = np.array([inputs])
    predicted_risk_score = model.predict(input_data)[0]

    # Classifying the risk score into categories
    if predicted_risk_score > 75:
        risk_category = "Low"
    elif 35 < predicted_risk_score <= 75:
        risk_category = "Medium"
    else:
        risk_category = "High"

    return predicted_risk_score, risk_category
