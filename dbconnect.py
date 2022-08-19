import json
from multiprocessing.sharedctypes import Value
from sqlalchemy import create_engine
from sqlalchemy import inspect
from ikeascraper import Scrape
from pandas import json_normalize
import pandas as pd

# create_engine(f"{database_type}+{db_api}://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABSE']}")
engine = create_engine('postgresql+psycopg2://postgres:Embassy7!@ikeascraper.cjqxq5ckwjtu.us-east-1.rds.amazonaws.com:5432/ikeascraper')
resultDf = pd.DataFrame()

bot = Scrape('chair')
product_db = bot.fetch()
for value in product_db.items():
    resultDf = resultDf.append(json_normalize(value))
print(resultDf)   

#import list from ikeascraper
resultDf.to_sql('resultDf', engine, if_exists='append')

inspect(engine).get_table_names()
