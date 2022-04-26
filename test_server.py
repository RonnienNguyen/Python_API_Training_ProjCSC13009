import pyodbc as odbc
import pandas as pd


"Step 1"
df = pd.read_csv('Real-Time_Traffic_Incident_Reports.csv')


df['Published Date'] = pd.to_datetime(df['Published Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
df['Status Date'] = pd.to_datetime(df['Published Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
df.drop(df.query('Location.isnull() | Status.isnull()').index, inplace=True)

columns = ['Traffic Report ID', 'Published Date', 'Issue Reported', 'Location',
            'Address', 'Status', 'Status Date']

df_data = df[columns]
records = df_data.values.tolist()


"""
Step 3.1 Create SQL Servre Connection String
"""
DRIVER = 'SQL Server'
SERVER_NAME = 'DESKTOP-2021XLB\SQLEXPRESS'
DATABASE_NAME = 'GG'

def connection_string(driver, server_name, database_name):
    conn_string = f"""
        DRIVER={{{driver}}};
        SERVER={server_name};
        DATABASE={database_name};
        Trust_Connection=yes;        
    """
    return conn_string

try:
    conn = odbc.connect(connection_string(DRIVER, SERVER_NAME, DATABASE_NAME))
except odbc.DatabaseError as e:
    print('Database Error:')
    print(str(e.value[1]))
except odbc.Error as e:
    print('Connection Error:')
    print(str(e.value[1]))


"""
Step 3.3 Create a cursor connection and insert records
"""

sql_insert = '''
    INSERT INTO Austin_Traffic_Incident 
    VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE())
'''

try:
    cursor = conn.cursor()
    cursor.executemany(sql_insert, records)
    cursor.commit();
except Exception as e:
    cursor.rollback()
    #print(str(e[1]))
finally:
    print('Task is complete.')
    cursor.close()
    conn.close()