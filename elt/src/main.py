import pandas as pd
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Create SQLAlchemy engine
engine = create_engine("postgresql+psycopg2://user:123@airline_oltp:5432/airline")

# date_to_compare = str(datetime.now()).split()[0]    # old

# today_str = str(datetime.now()).split()[0]
# today_date = datetime.strptime(today_str, '%Y-%m-%d').date()
# yesterday = today_date - timedelta(days=1)

date_to_compare = '2020-01-01'

table_names = [
    'airport', 'airplane', 'baggage', 'complaint',
    'employee', 'crew', 'flight', 'interaction',
    'miles', 'stay', 'passenger', 'promotion',
    'reservation', 'ticket'
]

os.makedirs('/home/hadoop/tmp_data', exist_ok=True)

for table in table_names:
    query = f"""
    SELECT * FROM {table}
    WHERE "IS_INSERTED" > %s OR "IS_MODIFIED" > %s;
    """

    df = pd.read_sql_query(query, engine, params=(date_to_compare, date_to_compare))
    df.to_csv(f'/home/hadoop/tmp_data/{table}.csv', index=False)


    
