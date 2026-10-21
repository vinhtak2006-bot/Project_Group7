import json
import pandas as pd
from sqlalchemy import create_engine

with open("../3.Data_Integration/Final_Data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

engine = create_engine("mysql+pymysql://root:@localhost:3306/homeoffice_db")

table_name = "products_reviews"
df.to_sql(table_name, con=engine, if_exists="replace", index=False)
