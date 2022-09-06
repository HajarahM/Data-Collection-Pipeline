import json
from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas as pd
import json

engine = create_engine('postgresql+psycopg2://postgres:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/ikeascraper')
# old_product_info = engine.execute('''SELECT * FROM public."productsDB"''').all()

# Retrieve all new data
jsonfile = pd.read_json('./raw_data/ikeadata.json') #Read the json file which will return a dictionary
productsDB = pd.DataFrame(jsonfile) #Convert that dictionary into a dataframe

#check for and drop duplicates  
# old_product_info = pd.read_sql_table('productsDB', con=engine)
# merged_products = pd.concat([old_product_info, new_products_info])
# new_unduplicated_products = merged_products.drop_duplicates(keep=False)
        
#update database
productsDB.to_sql('productsDB', engine, if_exists='append', index=False) # Use the to_sql method with pandas
print(productsDB) 
inspect(engine).get_table_names()