import json
from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas as pd

# create_engine(f"{database_type}+{db_api}://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABSE']}")
engine = create_engine('postgresql+psycopg2://postgres:AiCore2022!@ikeascraper.cjqxq5ckwjtu.us-east-1.rds.amazonaws.com:5432/ikeascraper')

jsonfile = pd.read_json('./raw_data/ikeadata.json') #Read the json file which will return a dictionary
productsDB = pd.DataFrame(jsonfile) #Convert that dictionary into a dataframe

print(productsDB)   

#import list from ikeascraper
productsDB.to_sql('productsDB', engine, if_exists='append') # Use the to_sql method with pandas

inspect(engine).get_table_names()
