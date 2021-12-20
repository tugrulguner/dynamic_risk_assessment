import pickle
from sklearn.metrics._plot.confusion_matrix import plot_confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

from diagnostics import model_predictions



###############Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 
output_model = os.path.join(config['output_model_path']) 

##############Function for reporting
def score_model():
    test_data = pd.DataFrame(
    columns=[
        'corporation',
        'lastmonth_activity',
        'lastyear_activity',
        'number_of_employees',
        'exited']
    )
    #calculate a confusion matrix using the test data and the deployed model
    #write the confusion matrix to the workspace
    for file in os.listdir(os.getcwd()+'/'+test_data_path+'/'):
        if file.endswith('.csv'):
            read_data = pd.read_csv(os.getcwd()+'/'+test_data_path+'/'+file)
            test_data = test_data.append(read_data)
        else:
            continue
    y = test_data.pop('exited').astype(int)
    X = test_data[['lastmonth_activity','lastyear_activity','number_of_employees']]
    predictions = model_predictions(X)
    c_matrix = metrics.confusion_matrix(y, predictions)
    sns.heatmap(c_matrix, annot=True, fmt='d')
    plt.savefig(os.getcwd()+'/'+output_model+'/'+'confusionmatrix.png')


if __name__ == '__main__':
    score_model()
