from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import json
import os
import diagnostics
from scoring import score_model


######################Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 

prediction_model = None


#######################Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():
    input_data = request.get_json('path')
    test_data = pd.read_csv(input_data)
    y = test_data.pop('exited').astype(int)
    X = test_data[['lastmonth_activity','lastyear_activity','number_of_employees']]
    predictions = diagnostics.model_predictions(X)
    return predictions

#######################Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def scoring():        
    score = score_model()
    return str(score)

#######################Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def stats():        
    df_summary = diagnostics.dataframe_summary()
    return str(df_summary)

#######################Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def exec_time():        
    exec_time = diagnostics.execution_time()
    return str(exec_time)

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
