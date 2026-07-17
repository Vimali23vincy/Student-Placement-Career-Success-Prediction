"""
PlacifyAI - Prediction Module
Loads trained models and makes predictions on new student data.
"""

import numpy as np
import pandas as pd
import joblib
import os

import streamlit as st

# No longer using FEATURES or CATEGORICAL_FEATURES from preprocessing here.
# Features will be dynamically aligned using loaded feature columns.


@st.cache_resource
def load_models(models_dir: str = "models"):
    """
    Load all trained models and feature columns list.

    Returns
    -------
    placement_model : RandomForestClassifier
        Model for placement status prediction.
    company_model : RandomForestClassifier
        Model for company type prediction.
    feature_columns : list
        List of feature columns used during model training.
    """
    placement_model = joblib.load(os.path.join(models_dir, "placement_model.pkl"))
    company_model = joblib.load(os.path.join(models_dir, "company_model.pkl"))
    feature_columns = joblib.load(os.path.join(models_dir, "feature_columns.joblib"))

    return placement_model, company_model, feature_columns


def prepare_input(student_data: dict, feature_columns: list) -> pd.DataFrame:
    """
    Prepare a single student's data for prediction.

    Parameters
    ----------
    student_data : dict
        Dictionary with feature names as keys and raw values.
    feature_columns : list
        List of feature columns used during model training.

    Returns
    -------
    input_df : pd.DataFrame
        Single-row DataFrame aligned with training features.
    """
    input_df = pd.DataFrame([student_data])

    # Apply pd.get_dummies to convert categoricals to dummies
    input_df = pd.get_dummies(input_df, dtype=int)

    # Reindex columns to match training feature columns exactly, filling missing ones with 0
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    return input_df


def predict_placement(student_data: dict, placement_model, feature_columns) -> dict:
    """
    Predict placement status for a student.

    Returns
    -------
    result : dict
        - status: "Placed" or "Not Placed"
        - probability: float (probability of placement)
    """
    input_df = prepare_input(student_data, feature_columns)

    prediction = placement_model.predict(input_df)[0]
    probabilities = placement_model.predict_proba(input_df)[0]

    status = "Placed" if prediction == 1 else "Not Placed"
    probability = probabilities[1]  # Probability of being placed

    return {
        "status": status,
        "probability": round(probability * 100, 1),
    }


def predict_company(student_data: dict, company_model, feature_columns) -> dict:
    """
    Predict company type for a placed student.

    Returns
    -------
    result : dict
        - company_type: "Product Based" or "Service Based"
        - probability: float (probability of product-based company)
    """
    input_df = prepare_input(student_data, feature_columns)

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
    placement_model, company_model, feature_columns = load_models(models_dir)

    # Step 1: Placement prediction
    placement_result = predict_placement(student_data, placement_model, feature_columns)

    result = {
        "placement_status": placement_result["status"],
        "placement_probability": placement_result["probability"],
        "company_type": "N/A",
        "company_confidence": None,
    }

    # Step 2: Company type (only if placed)
    if placement_result["status"] == "Placed":
        company_result = predict_company(student_data, company_model, feature_columns)
        result["company_type"] = company_result["company_type"]
        result["company_confidence"] = company_result["confidence"]

    return result
