# calorie_model.py — Final robust ML model for calorie prediction
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error
import os


# =========================================================
# Train and Save the Model
# =========================================================
def train_calorie_model(data_path="fitnessdataset_augmented.xlsx",
                        target="Current Calorie Intake",
                        out_dir="."):
    print(f"📂 Loading dataset from {data_path} ...")

    # Load dataset
    if data_path.endswith(".xlsx"):
        df = pd.read_excel(data_path)
    else:
        df = pd.read_csv(data_path)

    # Drop NA target values
    df = df.dropna(subset=[target])
    y = df[target]
    X = df.drop(columns=[target])

    # One-hot encode categorical features
    X = pd.get_dummies(X, drop_first=True)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Evaluate
    preds = model.predict(X_test_scaled)
    print(f"✅ R² Score: {r2_score(y_test, preds):.3f}")
    print(f"✅ MAE: {mean_absolute_error(y_test, preds):.2f} kcal")

    # Save model and scaler
    joblib.dump(model, os.path.join(out_dir, "calorie_model.pkl"))
    joblib.dump(scaler, os.path.join(out_dir, "scaler.pkl"))
    print("💾 Saved calorie_model.pkl and scaler.pkl successfully!")


# =========================================================
# Predict Calories (robust version)
# =========================================================
def predict_calories(input_dict,
                     model_path="calorie_model.pkl",
                     scaler_path="scaler.pkl"):
    """
    Predict calorie needs based on user input features.
    Works with all sklearn versions (auto-detects input columns).
    """
    import os
    import joblib
    import pandas as pd

    # ✅ Try current folder first, then fallback to script folder
    if not os.path.exists(model_path):
        model_path = os.path.join(os.path.dirname(__file__), "calorie_model.pkl")
    if not os.path.exists(scaler_path):
        scaler_path = os.path.join(os.path.dirname(__file__), "scaler.pkl")

    # ✅ Load trained model and scaler
    print(f"📁 Loading model from: {model_path}")
    print(f"📁 Loading scaler from: {scaler_path}")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    # ✅ Prepare input
    X = pd.DataFrame([input_dict])
    X = pd.get_dummies(X, drop_first=True)

    # ✅ Determine training columns robustly
    training_columns = getattr(model, "feature_names_in_", None)
    if training_columns is None:
        # Fallback: reload the dataset to get the same columns used in training
        if os.path.exists("fitnessdataset_augmented.xlsx"):
            df = pd.read_excel("fitnessdataset_augmented.xlsx")
        elif os.path.exists("fitnessdataset_augmented.csv"):
            df = pd.read_csv("fitnessdataset_augmented.csv")
        else:
            raise FileNotFoundError("⚠️ Dataset not found for feature reconstruction.")

        df = df.dropna(subset=["Current Calorie Intake"])
        X_train = df.drop(columns=["Current Calorie Intake"])
        X_train = pd.get_dummies(X_train, drop_first=True)
        training_columns = X_train.columns

    # ✅ Align columns safely
    for col in training_columns:
        if col not in X.columns:
            X[col] = 0
    X = X[training_columns]

    # ✅ Scale + predict
    X_scaled = scaler.transform(X)
    predicted = float(model.predict(X_scaled)[0])
    return predicted


# =========================================================
# Script Entrypoint (auto-trains if run directly)
# =========================================================
if __name__ == "__main__":
    train_calorie_model("fitnessdataset_augmented.xlsx")
