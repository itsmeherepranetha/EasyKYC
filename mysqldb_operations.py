import mysql.connector
import streamlit as st
import pandas as pd

create_db="""create database if not exists ekyc;"""
use_db = """use ekyc;"""
create_table="""
create table if not exists person_details(
id varchar(255),
create_time datetime,
name varchar(255),
father_name varchar(255),
dob datetime,
id_type varchar(255)
);
"""


# Establish a connection to MySQL Server
db_config = st.secrets["mysql"]
mydb = mysql.connector.connect(
    host=db_config["host"],
    port=int(db_config["port"]),
    user=db_config["user"],
    password=db_config["password"]
)
mycursor=mydb.cursor()
print("Connection Established")

mycursor.execute(create_db)
mycursor.execute(use_db)
mycursor.execute(create_table)
print("Database and Table created or verified.")

mydb = mysql.connector.connect(
    host=db_config["host"],
    port=int(db_config["port"]),
    user=db_config["user"],
    password=db_config["password"],
    database=db_config["database"]
)
mycursor=mydb.cursor()

def insert_records(text_info):
    try:
        mydb = mysql.connector.connect(
            host=db_config["host"],
            port=int(db_config["port"]),
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO person_details(id, name, father_name, dob, id_type) VALUES (%s, %s, %s, %s, %s)"
        value = (text_info['ID'],
            text_info['Name'],
            text_info["Father's Name"],
            text_info['DOB'], 
            text_info['ID Type']
            )
        mycursor.execute(sql, value)
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        mycursor.close()
        mydb.close()

def fetch_records(text_info):
    try:
        mydb = mysql.connector.connect(
            host=db_config["host"],
            port=int(db_config["port"]),
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM person_details WHERE id =%s"
        value = (text_info['ID'],)
        mycursor.execute(sql, value)
        result = mycursor.fetchall()
        if result:
            df = pd.DataFrame(result, columns=[desc[0] for desc in mycursor.description])
            return df
        else:
            return pd.DataFrame() 
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        mycursor.close()
        mydb.close()

def check_duplicacy(text_info):
    is_duplicate = False
    df =  fetch_records(text_info)
    if df.shape[0]>0:
        is_duplicate = True
    return is_duplicate

    