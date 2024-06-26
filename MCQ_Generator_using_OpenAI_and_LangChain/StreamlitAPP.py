import os
import json
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

#Reading json file
with open('Response.json', 'r') as file:
  response_json = json.load(file)

#Creating a title ffor the app
st.title("MCQs generator application with LangChain")

#Create a form using st.form
with st.form('user_inputs'):
  #File upload
  uploaded_file = st.file_uploader('Upload a PDF or text file')

  #Input Fields
  mcq_count = st.number_input('No. of MCQs', min_value = 3, max_value = 50)

  #Subject
  subject = st.text_input('Inser subject', max_chars = 20)

  #Quiz tone
  tone = st.text_input('Complexity level of questions', max_chars = 20, placeholder = 'simple')

  #Add button
  button = st.form_submit_button("Create MCQs")

  #Check if the button is clicked and all the fileds are input
  if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner('Loading...'):
      try:
        text = read_file(uploaded_file)
        #Count tokens and the cost of API call
        with gen_openai_callback as cb:
          response = generate_evaluate_chain(
            { 'text' : text,
             'number' : mcq_count,
             'subject' : subject,
             'tone' : tone,
             'response_json' : json.dumps(response_json)
             )
        #st.write(response)
      except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
      else:
        print(f'Total tokens : {cb.total_tokens}')
        print(f'Prompt tokens : {cb.prompt_tokens}')
        print(f'Completion tokens : {cb.completion_tokens}')
        print(f'Total cost : {cb.total_cost}')

        if isinstance(response, dict):
          #Extract quiz data from response
          quiz = response.get('quiz', None)
          if quiz is not None:
            table_data = get_table_data(quiz)
            if table_data is not None:
              df = pf.DataFrame(table_data)
              df.index = df.index + 1
              st.table(df)

              #Display the review in a text box
              st.text_area(label = 'review', value = response['review'])

            else:
              st.error("Error in table data")

        else:
          st.write(response)
          
