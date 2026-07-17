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
    "degree",
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

CATEGORICAL_FEATURES = ["branch", "degree"]
NUMERICAL_FEATURES = [f for f in FEATURES if f not in CATEGORICAL_FEATURES]


def load_data(path: str = "data/student_placement.csv") -> pd.DataFrame:
    """Load the student placement dataset."""
    df = pd.read_csv(path)
    return df


def prepare_placement_data(df: pd.DataFrame):
    """
    Prepare data for placement status prediction.

    Returns
    -------
    X : pd.DataFrame
        One-hot encoded feature matrix.
    y : pd.Series
        Binary target (1 = Placed, 0 = Not Placed).
    """
    # Map target
    if df[TARGET_PLACEMENT].dtype == object or df[TARGET_PLACEMENT].dtype == str:
        y = (df[TARGET_PLACEMENT] == "Placed").astype(int)
    else:
        y = df[TARGET_PLACEMENT].astype(int)

    # Select features and apply get_dummies
    X_raw = df[FEATURES].copy()
    X = pd.get_dummies(X_raw, dtype=int)

    return X, y


def prepare_company_data(df: pd.DataFrame):
    """
    Prepare data for company type prediction (placed students only).

    Returns
    -------
    X : pd.DataFrame
        One-hot encoded feature matrix (placed students only).
    y : pd.Series
        Binary target (1 = Product Based, 0 = Service Based).
    """
    # Filter to placed students only
    if df[TARGET_PLACEMENT].dtype == object or df[TARGET_PLACEMENT].dtype == str:
        placed_df = df[df[TARGET_PLACEMENT] == "Placed"].copy()
    else:
        placed_df = df[df[TARGET_PLACEMENT] == 1].copy()

    # Map target
    if placed_df[TARGET_COMPANY].dtype == object or placed_df[TARGET_COMPANY].dtype == str:
        y = (placed_df[TARGET_COMPANY] == "Product Based").astype(int)
    else:
        y = placed_df[TARGET_COMPANY].astype(int)

    # Select features and apply get_dummies
    X_raw = placed_df[FEATURES].copy()
    X = pd.get_dummies(X_raw, dtype=int)

    return X, y


def save_feature_columns(columns: list, path: str = "models/feature_columns.joblib"):
    """Save the list of feature columns to disk."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(columns, path)
    print(f"💾 Feature columns saved → {path}")


def load_feature_columns(path: str = "models/feature_columns.joblib") -> list:
    """Load the list of feature columns from disk."""
    return joblib.load(path)

