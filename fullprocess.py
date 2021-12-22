import json
import os
import sys
import pandas as pd
from sklearn import metrics
import pickle
import training
import scoring
import deployment
import diagnostics
import reporting

with open('config.json','r') as f:
    config = json.load(f) 

input_data_path = os.path.join(config['input_folder_path'])
dataset_csv_path = os.path.join(config['output_folder_path']) 
model_path = os.path.join(config['output_model_path'])
prod_folder_path = os.path.join(config['prod_deployment_path']) 


##################Check and read new data
with open(os.getcwd()+'/'+prod_folder_path+'/'+'ingestedfiles.txt','r') as f:
  read_data_files = f.read().rstrip()

continue_pr = False
for file in os.listdir(os.getcwd()+'/'+input_data_path+'/'):
  if file in read_data_files:
    continue
  else:
    os.system(f'python ingestion.py {input_data_path}')
    continue_pr = True
    break


#second, determine whether the source data folder has files that aren't listed in ingestedfiles.txt

##################Deciding whether to proceed, part 1
#if you found new data, you should proceed. otherwise, do end the process here
if continue_pr == False:
  sys.exit()

##################Checking for model drift
#check whether the score from the deployed model is different from the score from the model that uses the newest ingested data
with open(os.getcwd()+'/'+prod_folder_path+'/'+'latestscore.txt') as f:
  score = float(f.read().rsplit()[0])

data = pd.read_csv(os.getcwd()+'/'+dataset_csv_path+'/'+'finaldata.csv')
y = data.pop('exited').astype(int)
X = data[['lastmonth_activity','lastyear_activity','number_of_employees']]
for file in os.listdir(os.getcwd()+'/'+prod_folder_path):
    if file.endswith('.pkl'):
        model = pickle.load(open(os.getcwd()+'/'+prod_folder_path+'/'+file,'rb'))
predictions = model.predict(X)
# I will calculate the score here again, since scoring.py calculates the scores only with test data,
# not with latest ingested data. We didn't desgin scoring.py to take predictions and actual y as an input.
new_scores = metrics.f1_score(y, predictions)
##################Deciding whether to proceed, part 2
#if you found model drift, you should proceed. otherwise, do end the process here

if new_scores >= score:
  sys.exit()
##################Re-deployment
#if you found evidence for model drift, re-run the deployment.py script

os.system('python training.py')
os.system('python deployment.py')

##################Diagnostics and reporting
#run diagnostics.py and reporting.py for the re-deployed model

os.system('python reporting.py')
os.system('python apicalls.py')





