# 🎯 PlacifyAI – AI-Powered Placement Prediction Platform

> Predict student placement outcomes and company types using Machine Learning.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

## 📋 Overview

PlacifyAI is an AI-powered campus placement intelligence platform that uses **RandomForestClassifier** models to predict:

1. **Placement Status** – Whether a student will be Placed or Not Placed
2. **Company Type** – Whether the placement will be in a Product-Based or Service-Based company

## 🏗️ Project Structure

```
PlacifyAI/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md
├── data/
│   └── student_placement.csv
├── models/
│   ├── placement_model.pkl
│   ├── company_model.pkl
│   └── encoder.pkl
├── src/
│   ├── preprocessing.py    # Data loading & encoding
│   ├── training.py         # Model training pipeline
│   └── prediction.py       # Prediction inference
└── pages/
    ├── Dashboard.py        # Analytics dashboard
    └── Predictor.py        # Placement predictor
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train Models

```bash
cd src
python training.py
```

This will train both models with hyperparameter tuning and save them to `models/`.

### 3. Run the App

```bash
streamlit run app.py
```

## 📊 Features

### Dashboard Page
- 6 KPI metric cards (Total Students, Placement Rate, etc.)
- 7 interactive Plotly charts
- Sidebar filters (Branch, College Tier, Placement Status)
- Modern dark theme

### Predictor Page
- Professional input form with 11 features
- Two-step ML prediction pipeline
- Styled result cards with probability visualization

## 🤖 ML Pipeline

| Model | Target | Algorithm | Data |
|-------|--------|-----------|------|
| Model 1 | Placement Status | RandomForestClassifier | All students |
| Model 2 | Company Type | RandomForestClassifier | Placed students only |

**Pipeline includes:** Train/Test Split, GridSearchCV Hyperparameter Tuning, Cross-Validation, Feature Importance, Classification Report, Confusion Matrix.

## 📝 Version

**v1.0 – Phase 1**
