import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title = "Gemini Invoice Extractor")

os.environ['GOOGLE_API_KEY'] = "AIzaSyCaW7JGGWjiBRvq2DGl9uTIrptH7FzhFh8"

load_dotenv()

genai.configure()

#model = genai.GenerativeModel('gemini-1.5-flash')
#response = model.generate_content("Write a short story")
#print(response.text)

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [{"mime_type" : uploaded_file.type, "data" : bytes_data}]
        
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
#Streamlit app
st.header("Gemini Invoice Extractor Application")

input = st.text_input("Input Prompt : ", key = "input")
uploaded_file = st.file_uploader("Choose an Image file", type = ['jpg', 'jpeg', 'png'])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Uploaded Image", use_column_width = True) #Display uploaded image

submit = st.button("Tell me about the invoice")

#Prompt
input_prompt = """
You are an expert in understanding invoices regardless of the language in the invoices.
You will recieve input images of invoices and you will have to
answer questions based on the input image.
"""

#Submit botton clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    
    st.subheader("Response : ")
    st.write(response)