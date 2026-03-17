import pickle
import pandas as pd   

with open('model/model.pkl','rb') as f:
    main_model = pickle.load(f)

def predict_output(user_input: dict):
    input_df = pd.DataFrame([user_input])
    output = main_model.predict(
        input_df[['cluster','year','month','day','hour','dayofweek','isweekend']]
    )
    return round(output[0])