# HOW TO START THE PROJECT
# OPEN TERMINAL
# pipenv shell
# uvicorn main:app --reload
from fastapi import FastAPI, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from joblib import load 
import numpy as np
import pandas as pd
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
        # Seperate target variable
        # Initialize a StandardScaler object
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df)
        print(X_scaled.shape)
        # feed into model
        model = load("stacking_model.joblib")
        # result
        result = model.predict(X_scaled)
        message = "you have heart diseases" if result[0] else "congratulation you dont have heart disease"
        print(message)
        return {"message": message, "heart_disease": True if result[0] == 1 else False}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
