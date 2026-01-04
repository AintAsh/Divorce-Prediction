from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle

# --------------------------------------------------
# App init
# --------------------------------------------------
app = FastAPI(
    title="Divorce Prediction API",
    description="Predict divorce risk using a trained Random Forest model",
    version="1.0"
)

# --------------------------------------------------
# Load dataset (for schema & categories)
# --------------------------------------------------
df = pd.read_csv("divorce_df.csv")
TARGET_COL = "divorced"
FEATURES = df.drop(columns=[TARGET_COL]).columns.tolist()

# --------------------------------------------------
# Load model
# --------------------------------------------------
with open("divorce_model.pkl", "rb") as f:
    loaded_obj = pickle.load(f)

if isinstance(loaded_obj, dict):
    model = loaded_obj["model"]
    FEATURES = loaded_obj["features"]
else:
    model = loaded_obj

# --------------------------------------------------
# Input schema
# --------------------------------------------------
class DivorceInput(BaseModel):
    age_at_marriage: float
    marriage_duration_years: float
    num_children: float
    education_level: str
    employment_status: str
    combined_income: float
    religious_compatibility: str
    cultural_background_match: str
    communication_score: float
    conflict_frequency: float
    conflict_resolution_style: str
    financial_stress_level: float
    mental_health_issues: str
    infidelity_occurred: str
    counseling_attended: str
    social_support: float
    shared_hobbies_count: float
    marriage_type: str
    pre_marital_cohabitation: str
    domestic_violence_history: str
    trust_score: float

# --------------------------------------------------
# Encoders
# --------------------------------------------------
def encode_binary(value: str) -> int:
    return 1 if str(value).lower() in ["yes", "true", "1"] else 0

def encode_categorical(feature: str, value: str) -> int:
    categories = (
        df[feature]
        .astype("category")
        .cat.categories
        .tolist()
    )
    mapping = {str(cat).lower(): i for i, cat in enumerate(categories)}
    return mapping.get(str(value).lower(), 0)

# --------------------------------------------------
# Routes
# --------------------------------------------------
@app.get("/")
def home():
    return {"status": "API running", "docs": "/docs"}

@app.post("/predict/")
def predict_divorce(data: DivorceInput):
    try:
        raw = data.dict()
        processed = {}

        for feature in FEATURES:
            value = raw[feature]

            # binary yes/no
            if isinstance(value, str) and value.lower() in ["yes", "no"]:
                processed[feature] = encode_binary(value)

            # numeric
            elif pd.api.types.is_numeric_dtype(df[feature]):
                processed[feature] = float(value)

            # categorical
            else:
                processed[feature] = encode_categorical(feature, value)

        input_df = pd.DataFrame([processed])

        prediction = int(model.predict(input_df)[0])
        probability = float(model.predict_proba(input_df)[0][1])

        return {
            "prediction": prediction,
            "probability": round(probability, 4),
            "risk_level": (
                "High Relationship Stress"
                if prediction == 1
                else "Low Relationship Stress"
            )
        }

    except Exception as e:
        return {"error": "Prediction failed", "message": str(e)}
