import json
import os
import sys
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


##################Deciding whether to proceed, part 2
#if you found model drift, you should proceed. otherwise, do end the process here



##################Re-deployment
#if you found evidence for model drift, re-run the deployment.py script

##################Diagnostics and reporting
#run diagnostics.py and reporting.py for the re-deployed model







