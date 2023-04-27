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
smoker: bool = Form(...),
BPMeds: bool = Form(...),
prevalentStroke: bool = Form(...),
prevalentHyp: bool = Form(...),
diabetes: bool = Form(...),
sysBP: bool = Form(...),
diaBP: bool = Form(...),
gender: str = Form(...),
BMI: int = Form(...),
heartRate: int = Form(...),
):
    try:
        is_male = True if gender == "male" else False
        columns = ['is_male','age_yrs','education_yrs','is_smoker','cigsPerDay','is_on_bp_meds','has_history_of_stroke','has_hypertension','has_diabetes','tot_chol','systolic_blood_pressure','diastolic_blood_pressure','BMI','heart_rate_bpm','glucose']
        data = [is_male, age, education_yrs, smoker, cigsPerDay, BPMeds, prevalentStroke, prevalentHyp, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose]
        data = pd.Series(data, index=columns)
        print(data)
        # preprocessing
        df = pd.DataFrame([data], columns=columns)
        df = encoding(df)
        # Seperate target variable
        # Initialize a StandardScaler object
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df)
        print(X_scaled.shape)

        # feed into model
        model = load("RFC_MLP_optimized_best_model.joblib")

        # result
        result = model.predict(X_scaled)
        message = "you have heart disease" if result[0] == 1 else "congratulation you dont have heart disease"
        print(message)

        return {"message": message, "heart_disease": True if result[0] == 1 else False}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
def encoding(df):
    # perform one hot encoding on the education column using get_dummies()
    education_dummies = pd.get_dummies(df['education_yrs'], prefix='education_yrs')

    # concatenate the education dummies DataFrame with the original DataFrame
    df = pd.concat([df, education_dummies], axis=1)

    # drop the original education column
    df = df.drop('education_yrs', axis=1)

    columns_might_missing = [
        "education_yrs_1",
        "education_yrs_2",
        "education_yrs_3",
        "education_yrs_4"
    ]

    for column in columns_might_missing:
        if column not in df:
            df[column] = 0
    return df
