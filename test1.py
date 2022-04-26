import pyodbc
import pandas as pd

# print(pyodbc.drivers())

conn = pyodbc.connect(
    Trusted_Connected = "Yes",
    Driver = {'ODBC Driver 17 for SQL Server'},
    Server = "DESKTOP-2021XLB",
    Database = "SQLTurtorial"
)

cursor = conn.cursor()