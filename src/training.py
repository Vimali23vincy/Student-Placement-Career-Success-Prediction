"""
PlacifyAI - Training Module
Trains RandomForestClassifier models for placement status and company type prediction.
Includes hyperparameter tuning, cross-validation, and evaluation.
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    cross_val_score,
)
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
)

from preprocessing import (
    load_data,
    prepare_placement_data,
    prepare_company_data,
    save_feature_columns,
    FEATURES,
)


# ── Hyperparameter Grid ────────────────────────────────────────────────────────
PARAM_GRID = {
    "n_estimators": [100, 200, 300],
    "max_depth": [10, 15, 20, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["sqrt", "log2"],
}

# Lighter grid for faster tuning while still finding good params
PARAM_GRID_LIGHT = {
    "n_estimators": [100, 200],
    "max_depth": [10, 20, None],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2],
    "max_features": ["sqrt"],
}

MODELS_DIR = "models"


def train_model(X_train, y_train, param_grid=None, cv=5):
    """
    Train a RandomForestClassifier with GridSearchCV hyperparameter tuning.

    Parameters
    ----------
    X_train : pd.DataFrame
        Training features.
    y_train : pd.Series
        Training target.
    param_grid : dict or None
        Hyperparameter grid for GridSearchCV.
    cv : int
        Number of cross-validation folds.

    Returns
    -------
    best_model : RandomForestClassifier
        Best estimator from GridSearchCV.
    grid_results : GridSearchCV
        Full grid search results.
    """
    if param_grid is None:
        param_grid = PARAM_GRID_LIGHT

    rf = RandomForestClassifier(random_state=42, n_jobs=-1)

    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=cv,
        scoring="accuracy",
        n_jobs=-1,
        verbose=1,
    )
    grid_search.fit(X_train, y_train)

    print(f"\n✅ Best Parameters: {grid_search.best_params_}")
    print(f"✅ Best CV Accuracy: {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_, grid_search


def evaluate_model(model, X_test, y_test, label_names=None):
    """
    Evaluate a trained model and print metrics.

    Parameters
    ----------
    model : RandomForestClassifier
        Trained model.
    X_test : pd.DataFrame
        Test features.
    y_test : pd.Series
        Test target.
    label_names : list or None
        Human-readable class names.

    Returns
    -------
    metrics : dict
        Dictionary with accuracy, classification_report, confusion_matrix.
    """
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"\n📊 Test Accuracy: {acc:.4f}")
    print("\n📋 Classification Report:")
    report = classification_report(y_test, y_pred, target_names=label_names)
    print(report)

    cm = confusion_matrix(y_test, y_pred)
    print("🔢 Confusion Matrix:")
    print(cm)

    # Cross-validation score on full test set
    cv_scores = cross_val_score(model, X_test, y_test, cv=min(5, len(y_test) // 5), scoring="accuracy")
    print(f"\n🔁 Cross-Val Scores: {cv_scores}")
    print(f"🔁 Mean CV Score: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Feature importance
    importance = pd.DataFrame(
        {"feature": X_test.columns, "importance": model.feature_importances_}
    ).sort_values("importance", ascending=False)
    print("\n🏆 Feature Importance:")
    print(importance.to_string(index=False))

    return {
        "accuracy": acc,
        "classification_report": report,
        "confusion_matrix": cm,
        "cv_scores": cv_scores,
        "feature_importance": importance,
    }


def save_model(model, path):
    """Save a trained model to disk."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"💾 Model saved → {path}")


def main():
    """Full training pipeline."""
    print("=" * 60)
    print("  PlacifyAI – Model Training Pipeline")
    print("=" * 60)

    # ── Load Data ──────────────────────────────────────────────────────────
    print("\n📂 Loading dataset...")
    df = load_data()
    print(f"   Dataset shape: {df.shape}")

    # ── Model 1: Placement Status ──────────────────────────────────────────
    print("\n" + "─" * 60)
    print("  MODEL 1: Placement Status Prediction")
    print("─" * 60)

    X_placement, y_placement = prepare_placement_data(df)
    X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
        X_placement, y_placement, test_size=0.2, random_state=42, stratify=y_placement
    )

    print(f"\n   Training set: {X_train_p.shape[0]} | Test set: {X_test_p.shape[0]}")
    print("   Tuning hyperparameters...")

    placement_model, _ = train_model(X_train_p, y_train_p)
    placement_metrics = evaluate_model(
        placement_model, X_test_p, y_test_p, label_names=["Not Placed", "Placed"]
    )

    # ── Model 2: Company Type ──────────────────────────────────────────────
    print("\n" + "─" * 60)
    print("  MODEL 2: Company Type Prediction (Placed Students Only)")
    print("─" * 60)

    X_company, y_company = prepare_company_data(df)
    X_company = X_company.reindex(columns=X_placement.columns, fill_value=0)
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
        X_company, y_company, test_size=0.2, random_state=42, stratify=y_company
    )

    print(f"\n   Training set: {X_train_c.shape[0]} | Test set: {X_test_c.shape[0]}")
    print("   Tuning hyperparameters...")

    company_model, _ = train_model(X_train_c, y_train_c)
    company_metrics = evaluate_model(
        company_model, X_test_c, y_test_c, label_names=["Service Based", "Product Based"]
    )

    # ── Save Artifacts ─────────────────────────────────────────────────────
    print("\n" + "─" * 60)
    print("  Saving Models & Encoders")
    print("─" * 60)

    save_model(placement_model, os.path.join(MODELS_DIR, "placement_model.pkl"))
    save_model(company_model, os.path.join(MODELS_DIR, "company_model.pkl"))
    save_feature_columns(X_placement.columns.tolist(), os.path.join(MODELS_DIR, "feature_columns.joblib"))

    print("\n✅ Training complete! All models saved to models/")
    print("=" * 60)


if __name__ == "__main__":
    main()
