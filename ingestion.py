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
def merge_multiple_dataframe(input_folder_path):
    ingestedlist = []
    df = pd.DataFrame(
        columns=['corporation',
        'lastmonth_activity',
        'lastyear_activity',
        'number_of_employees',
        'exited']
        )
    for file in os.listdir(os.getcwd()+'/'+input_folder_path):
        try:
            read_data = pd.read_csv(os.getcwd()+'/'+input_folder_path+'/'+file)
            df = df.append(read_data).reset_index(drop=True)
            ingestedlist.append(file)
        except pd.errors.EmptyDataError:
            continue
    
    # Drop duplicated 
    df.drop_duplicates(inplace=True, ignore_index=True)

    # Create output folder if not exist and save files
    if os.path.isdir(os.getcwd()+'/'+output_folder_path):
        df.to_csv(os.getcwd()+'/'+output_folder_path+'/finaldata.csv', index = False)
        with open(os.getcwd()+'/'+output_folder_path+'/ingestedfiles.txt', 'w') as f:
            for el in ingestedlist:
                f.write(el+'\n')
    else:
        os.mkdir(os.getcwd()+'/'+output_folder_path)
        df.to_csv(os.getcwd()+'/'+output_folder_path+'/finaldata.csv', index=False)
        with open(os.getcwd()+'/'+output_folder_path+'/ingestedfiles.txt', 'w') as f:
            for el in ingestedlist:
                f.write(el+'\n')

if __name__ == '__main__':
    merge_multiple_dataframe(input_folder_path)
