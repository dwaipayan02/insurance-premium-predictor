from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.predict import predict_output,model,MODEL_VERSION
from schema.prediction_response import PredictionResponse
import pandas as pd
from schema.user_input import UserInput
app = FastAPI()



@app.get('/') #this is human readable machine cannot understand this
def home():
    return{'message':'Insurance Premium Prediction API'}

@app.get('/health')#this is for when you host it on cloud platform the machine can read the api si working
def health_check():
    return{
        'status':'OK',
        'version' : MODEL_VERSION }



@app.post('/predict' ,response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={'predicted_category': prediction})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))
