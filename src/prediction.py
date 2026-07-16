"""
PlacifyAI - Prediction Module
Loads trained models and makes predictions on new student data.
"""

import numpy as np
import pandas as pd
import joblib
import os

import streamlit as st

from preprocessing import FEATURES, CATEGORICAL_FEATURES


@st.cache_resource
def load_models(models_dir: str = "models"):
    """
    Load all trained models and encoders.

    Returns
    -------
    placement_model : RandomForestClassifier
        Model for placement status prediction.
    company_model : RandomForestClassifier
        Model for company type prediction.
    encoder : dict
        Fitted label encoders.
    """
    placement_model = joblib.load(os.path.join(models_dir, "placement_model.pkl"))
    company_model = joblib.load(os.path.join(models_dir, "company_model.pkl"))
    encoder = joblib.load(os.path.join(models_dir, "encoder.pkl"))

    return placement_model, company_model, encoder


def prepare_input(student_data: dict, encoder: dict) -> pd.DataFrame:
    """
    Prepare a single student's data for prediction.

    Parameters
    ----------
    student_data : dict
        Dictionary with feature names as keys and raw values.
    encoder : dict
        Fitted label encoders for categorical features.

    Returns
    -------
    input_df : pd.DataFrame
        Single-row DataFrame ready for model prediction.
    """
    input_df = pd.DataFrame([student_data])

    # Encode categorical features
    for col in CATEGORICAL_FEATURES:
        if col in input_df.columns:
            input_df[col] = encoder[col].transform(input_df[col].astype(str))

    # Ensure correct feature order
    input_df = input_df[FEATURES]

    return input_df


def predict_placement(student_data: dict, placement_model, encoder) -> dict:
    """
    Predict placement status for a student.

    Returns
    -------
    result : dict
        - status: "Placed" or "Not Placed"
        - probability: float (probability of placement)
    """
    input_df = prepare_input(student_data, encoder)

    prediction = placement_model.predict(input_df)[0]
    probabilities = placement_model.predict_proba(input_df)[0]

    status = "Placed" if prediction == 1 else "Not Placed"
    probability = probabilities[1]  # Probability of being placed

    return {
        "status": status,
        "probability": round(probability * 100, 1),
    }


def predict_company(student_data: dict, company_model, encoder) -> dict:
    """
    Predict company type for a placed student.

    Returns
    -------
    result : dict
        - company_type: "Product Based" or "Service Based"
        - probability: float (probability of product-based company)
    """
    input_df = prepare_input(student_data, encoder)

    prediction = company_model.predict(input_df)[0]
    probabilities = company_model.predict_proba(input_df)[0]

    company_type = "Product Based" if prediction == 1 else "Service Based"
    probability = probabilities[prediction]

    return {
        "company_type": company_type,
        "confidence": round(probability * 100, 1),
    }


def predict_student(student_data: dict, models_dir: str = "models") -> dict:
    """
    Full prediction pipeline for a single student.

    Step 1: Predict placement status.
    Step 2: If placed, predict company type.

    Returns
    -------
    result : dict
        - placement_status: "Placed" or "Not Placed"
        - placement_probability: float
        - company_type: str or "N/A"
        - company_confidence: float or None
    """
    placement_model, company_model, encoder = load_models(models_dir)

    # Step 1: Placement prediction
    placement_result = predict_placement(student_data, placement_model, encoder)

    result = {
        "placement_status": placement_result["status"],
        "placement_probability": placement_result["probability"],
        "company_type": "N/A",
        "company_confidence": None,
    }

    # Step 2: Company type (only if placed)
    if placement_result["status"] == "Placed":
        company_result = predict_company(student_data, company_model, encoder)
        result["company_type"] = company_result["company_type"]
        result["company_confidence"] = company_result["confidence"]

    return result
