## Process Automated Dynamic Risk Assessment Project

This project aims to automate the dynamic risk assessment process using continuous monitoring of the ingested data, model, score to catch any model drift, data instability, and integration issues
on the way by using live API for monitoring and diagnosis. The whole system is operated under an automation script that is run periodically.

After setting the config.json with the proper path locations, which should be changed manually
from initial data to source data when you allow system to receive inputs, data ingestion is performed.
It automatically reads the specified input data folder first, and appends each csv file it finds to a pandas
dataframe and saves the resulting dataset as finaldata.csv into specified directory in config.json. As a final step, 
script will write the ingested data files into a text file as ingestedfiles.txt. This is a necessary step to track
ingested files to decide if any new file is appeared on the specified folder. Therefore, this is an
automated process that handles each new input file whenever it drops to any of these specified folders.

Next step is performing training and scoring for the prepared data. When the training is done, which we used
a simple Logistic Regression, it saves the model as pickle file to production folder. Likewise, scoring follows
the training but this time it uploads the saved model and uses test data to compute f1 score on the predictions.
It then saves the resulting score to a text file called latestscore.txt. This part is important because
automation process will check this text file each time when new data is received and will try to decide
if there is a model drift or not.

Afterwards, deployment script will move model pickle, latest score text and ingestedfiles text files to a 
production folder, again specified by the config.json. This step is crucial for moving re-trained model, score,
and ingestedfile text files to production folder each time it performs.

Next step involves the use of API (Flask here) endpoints to perform diagnostics on this automated system. 
By using API in app.py file, we call diagnostics module and perform predictions, dataframe summary,
current score, execution time of training and ingestion processes using ingested data and then also we check 
outdated dependencies. All of these results are then directed to specified end points as a part of the 
automation process since apicalls.py file will send request to these end points and then will save the
response to a text file as apireturns.txt. This part is also crucial for automation because here API is used to
monitor and diagnose the ongoing automation system on the way since it checks and saves the latest prediction results, 
dataframe statistics, diagnose the running time of training and ingestion.

Finally, fullprocess.py file acts as a maestro that drives this automation process. It first checks whether there is any
new input data to perform data ingestion. If there is any new input, it decides to perform ingestion or else stops 
running the code. When it performs data ingestion, it uploads the latest model pickle file, performs prediction and 
then calculates the new score. Here, again, script checks whether new score is higher than the current one or not.
If it is higher, stops the execution, else, it decides there is a model drift and then executes training, scoring, 
and deployment again. Finally, when these new model and score files are uploaded to production folder, it performs
reporting, which saves confusion matrix into production folder, and finally apicalls again to monitor and diagnose
the automated process.

this fullprocess.py script should run periodically in a desired schedule, which crontab can be used easily for this job.




