"""
PlacifyAI - Preprocessing Module
Handles data loading, cleaning, encoding, and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# ── Feature Configuration ──────────────────────────────────────────────────────
FEATURES = [
    "college_tier",
    "branch",
    "cgpa",
    "backlog_history",
    "DSA_problems_solved",
    "GitHub_repos",
    "internships_completed",
    "resume_score",
    "communication_skills",
    "aptitude_score",
    "hackathons_participated",
]

TARGET_PLACEMENT = "placement_status"
TARGET_COMPANY = "company_type"

CATEGORICAL_FEATURES = ["branch"]
NUMERICAL_FEATURES = [f for f in FEATURES if f not in CATEGORICAL_FEATURES]


def load_data(path: str = "data/student_placement.csv") -> pd.DataFrame:
    """Load the student placement dataset."""
    df = pd.read_csv(path)
    # Keep only the columns we need
    required_cols = FEATURES + [TARGET_PLACEMENT, TARGET_COMPANY]
    df = df[required_cols].copy()
    return df


def encode_features(df: pd.DataFrame, encoder: dict | None = None, fit: bool = True):
    """
    Encode categorical features using LabelEncoder.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with raw features.
    encoder : dict or None
        Pre-fitted encoders. If None and fit=True, new encoders are created.
    fit : bool
        Whether to fit encoders or use existing ones.

    Returns
    -------
    df_encoded : pd.DataFrame
        Dataframe with encoded categorical features.
    encoder : dict
        Dictionary of fitted LabelEncoders.
    """
    df_encoded = df.copy()

    if encoder is None:
        encoder = {}

    for col in CATEGORICAL_FEATURES:
        if fit:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            encoder[col] = le
        else:
            le = encoder[col]
            df_encoded[col] = le.transform(df_encoded[col].astype(str))

    return df_encoded, encoder


def prepare_placement_data(df: pd.DataFrame):
    """
    Prepare data for placement status prediction.

    Returns
    -------
    X : pd.DataFrame
        Feature matrix.
    y : pd.Series
        Binary target (1 = Placed, 0 = Not Placed).
    encoder : dict
        Fitted label encoders for categorical features.
    """
    df_encoded, encoder = encode_features(df, fit=True)

    X = df_encoded[FEATURES]
    y = (df_encoded[TARGET_PLACEMENT] == "Placed").astype(int)

    return X, y, encoder


def prepare_company_data(df: pd.DataFrame, encoder: dict):
    """
    Prepare data for company type prediction (placed students only).

    Returns
    -------
    X : pd.DataFrame
        Feature matrix (placed students only).
    y : pd.Series
        Binary target (1 = Product Based, 0 = Service Based).
    """
    placed_df = df[df[TARGET_PLACEMENT] == "Placed"].copy()
    placed_encoded, _ = encode_features(placed_df, encoder=encoder, fit=False)

    X = placed_encoded[FEATURES]
    y = (placed_encoded[TARGET_COMPANY] == "Product Based").astype(int)

    return X, y


def save_encoder(encoder: dict, path: str = "models/encoder.pkl"):
    """Save label encoders to disk."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(encoder, path)


def load_encoder(path: str = "models/encoder.pkl") -> dict:
    """Load label encoders from disk."""
    return joblib.load(path)
