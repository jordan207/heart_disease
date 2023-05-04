# HOW TO START THE PROJECT
# OPEN TERMINAL
# pipenv shell
# uvicorn main:app --reload
from fastapi import FastAPI, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from joblib import load
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict")
async def predict(
    age: int = Form(...),
    education_yrs: int = Form(...),
    totChol: int = Form(...),
    cigsPerDay: int = Form(...),
    glucose: int = Form(...),
    sysBP: int = Form(...),
    diaBP: int = Form(...),
    smoker: bool = Form(...),
    BPMeds: bool = Form(...),
    prevalentStroke: bool = Form(...),
    prevalentHyp: bool = Form(...),
    diabetes: bool = Form(...),
    gender: str = Form(...),
    BMI: float = Form(...),
    heartRate: int = Form(...),
):
    try:
        is_male = True if gender == "male" else False
        smoker = 1 if smoker == True else 0
        BPMeds = 1 if BPMeds == True else 0
        prevalentStroke = 1 if prevalentStroke == True else 0
        prevalentHyp = 1 if prevalentHyp == True else 0
        diabetes = 1 if diabetes == True else 0
        columns = ['is_male', 'age_yrs', 'education_yrs', 'is_smoker', 'cigsPerDay', 'is_on_bp_meds', 'has_history_of_stroke', 'has_hypertension',
                   'has_diabetes', 'tot_chol', 'systolic_blood_pressure', 'diastolic_blood_pressure', 'BMI', 'heart_rate_bpm', 'glucose']
        data = [is_male, age, education_yrs, smoker, cigsPerDay, BPMeds, prevalentStroke,
                prevalentHyp, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose]
        data = pd.Series(data, index=columns)
        print(data)
        # preprocessing
        df = pd.DataFrame([data], columns=columns)

        education_dummies = pd.get_dummies(
            df['education_yrs'], prefix='education_yrs')
        education_dummies = add_missing_features(education_dummies)

        df = df.drop('education_yrs', axis=1)

        # Initialize a StandardScaler object
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df)

        print(X_scaled)
        # feed into model
        print(df)
        print(education_dummies)
        # education_dummies to numpy nd array
        education_dummies = education_dummies.to_numpy()

        # concat education_dummies to X_scaled

        df = np.concatenate((X_scaled, education_dummies), axis=1)

        model = load("RFC_MLP_optimized_best_model.joblib")

        # result
        result = model.predict(df)
        print(result)
        print(result[0])
        message = "You have a HIGH chance of having heart disease in 10 years." if result[
            0] == 1 else "You have a LOW chance of having heart disease in 10 years."
        print(message)
        return {"message": message, "heart_disease": True if result[0] == 1 else False}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def add_missing_features(dummies):
    columns_might_missing = [
        "education_yrs_1", "education_yrs_2", "education_yrs_3", "education_yrs_4"
    ]
    for column in columns_might_missing:
        if column not in dummies:
            dummies[column] = 0
    return dummies
