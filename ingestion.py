import pandas as pd
import numpy as np
import os
import json
from datetime import datetime




#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']



#############Function for data ingestion
def merge_multiple_dataframe():
    df = pd.DataFrame(columns=['corporation','lastmonth_activity','lastyear_activity','number_of_employees','exited'])
    for file in os.listdir(os.getcwd()+'/'+input_folder_path):
        try:
            read_data = pd.read_csv(os.getcwd()+'/'+input_folder_path+'/'+file)
            df = df.append(read_data).reset_index(drop=True)
        except pd.errors.EmptyDataError:
            continue
    
    if os.path.isdir(os.getcwd()+'/'+output_folder_path):
        df.to_csv(os.getcwd()+'/'+output_folder_path+'/finaldata.csv')
    else:
        os.mkdir(os.getcwd()+'/'+output_folder_path)
        df.to_csv(os.getcwd()+'/'+output_folder_path+'/finaldata.csv')

if __name__ == '__main__':
    merge_multiple_dataframe()
