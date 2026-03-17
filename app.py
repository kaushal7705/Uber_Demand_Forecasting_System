from fastapi import FastAPI
from model.main_model import predict_output
from schema.User_input import UserInput
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get('/')
def home():
    return {'message': 'Uber Demand Forecasting App'}

@app.post('/prediction')
def predict_demand(data: UserInput):
    user_input = {
        'cluster': data.cluster,
        'year': data.year,
        'month': data.month,
        'day': data.day,
        'hour': data.hour,
        'dayofweek': data.day_of_week,
        'isweekend': data.is_weekend
    }

    try:
        prediction = predict_output(user_input)

        return {
            "Predicted_demand": prediction
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})