import pandas as pd 

import os
import chardet

path = './cities'

files = []

for file in os.listdir(path):
    if file.endswith(".csv"):
        files.append(os.path.join(path, file))

for i in files:
    print(i)
    i = str(i)
    with open(i, 'rb') as f:
        # try:    
        result = chardet.detect(f.read())
        df = pd.read_csv(i, error_bad_lines=False, encoding=result['encoding'])
        cols = df.columns.tolist()
        df = df[['Category', 'Company_Name', 'Company_Website', 'Company_link', 'Address', 
                'Areas_Served', 'Awards', 'Company_Description', 'Job_Cost', 
                'License_number', 'Number_of_Reviews', 'Number_of_stars', 'Phone_Number','Phone2', 
                'Services_provided', 'City', 'Profile_img', 'Background_img']]
        df.to_csv(i, index=False)
        # except:
        #     pass
# print(df)