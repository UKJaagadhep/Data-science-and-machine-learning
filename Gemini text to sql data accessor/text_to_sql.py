from dotenv import load_dotenv
import os
import streamlit as st
import sqlite3
import google.generativeai as genai
import time

st.set_page_config(page_title = "Retrieve SQL query using text")

os.environ['GOOGLE_API_KEY'] = "AIzaSyCaW7JGGWjiBRvq2DGl9uTIrptH7FzhFh8"
load_dotenv()

genai.configure()

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

def read_and_execute_sql_query(sql, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    for row in rows:
        print(row)
    return rows
    
prompt = [
    """
    You are in expert in converting English questions to SQL code!
    The SQL database has the name STUDENT.db and the table name is STUDENT and has the following columns - NAME, CLASS, SECTION \n\n
    For example, \nExample 1 - How many entries of records are present?, the SQL command will be something
    like this SELECT COUNT(*) FROM STUDENT; \nExample 2 - Tell me all the students studying in DS class? the SQL command
    will be something like this SELECT * FROM STUDENT where CLASS = 'DS';
    also the sql code should not have ''' in beginning or end and sql word in output
    """
]

#Streamlit app
st.header("Gemini app to retrieve SQL data using text")

question = st.text_input("Input : ", key = "input")

submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question, prompt)
    response = read_and_execute_sql_query(response, "E:\\Downloads\\text to sql query -  gemini\\STUDENT.db")
    st.subheader("Response : ")
    for row in response:
        print(row)
        st.write(row)
