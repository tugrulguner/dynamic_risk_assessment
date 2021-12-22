
import pandas as pd
import numpy as np
import pickle
import timeit
import ast
import subprocess
import os
import json

##################Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path'])
prod_path = os.path.join(config['prod_deployment_path'])

##################Function to get model predictions
def model_predictions(dataset):
    for file in os.listdir(os.getcwd()+'/'+prod_path):
        if file.endswith('.pkl'):
            model = pickle.load(open(os.getcwd()+'/'+prod_path+'/'+file,'rb'))
    predictions = model.predict(dataset)
    return predictions

##################Function to get summary statistics
def dataframe_summary():
    data = pd.DataFrame(
    columns=[
        'corporation',
        'lastmonth_activity',
        'lastyear_activity',
        'number_of_employees',
        'exited']
    )
    for file in os.listdir(os.getcwd()+'/'+dataset_csv_path):
        if file.endswith('.csv'):
            data = pd.read_csv(os.getcwd()+'/'+dataset_csv_path+'/'+file)
    summary_statistics = [
        data.mean(skipna=True),
        data.median(skipna=True),
        data.std(skipna=True)
    ]
    nan_perc = data.isna().sum()/data.shape[0]
    print('summary statistics: ', summary_statistics)
    print('Nan values percentage: ', nan_perc)
    return str([summary_statistics, nan_perc])

#################Function to get timings
def execution_time():
    
    training_time_st = timeit.default_timer()
    subprocess.run(['python', 'training.py'])
    training_time = timeit.default_timer()-training_time_st
    
    ingestion_time_st = timeit.default_timer()
    subprocess.run(['python', 'ingestion.py'])
    ingestion_time = timeit.default_timer()-ingestion_time_st

    print([training_time, ingestion_time])
    return str([training_time, ingestion_time])

##################Function to check dependencies
def outdated_packages_list():
    outdated = subprocess.run(['pip','list','--outdated'])
    return outdated


# if __name__ == '__main__':
#     model_predictions()
#     dataframe_summary()
#     execution_time()
#     outdated_packages_list()





    
