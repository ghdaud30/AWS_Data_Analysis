import json
from datetime import datetime
from pytz import timezone
import pandas as pd
import os
import boto3

AWS_ACCESS_KEY_id = 'AKIA5ZPWZPVB2MVLSBN5'
AWS_ACCESS_KEY_SECRET = '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'

# set AWS credentials
s3r = boto3.resource('s3',
                     aws_access_key_id = AWS_ACCESS_KEY_id,
                     aws_secret_access_key=AWS_ACCESS_KEY_SECRET)
bucket = s3r.Bucket('real-estate555-bucket')

data = pd.DataFrame({
    "a" :[1,2,3],
    "b":['a','b','c']
})

def lambda_handler(event,context):
    current_time = datetime.now(timezone('Asia/Seoul'))
    print(current_time)
    
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    
    file_name = 'apart_trans_' + formatted_time + '.csv'
    
    data.to_csv('/tmp/python_test.csv')
    
    bucket.upload_file('/tmp/python_test.csv',file_name)
    
    return {'statusCode' : 200,
            'body' : json.dumps('Success !')}
     
