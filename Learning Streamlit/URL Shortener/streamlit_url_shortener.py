import streamlit as st
import pyshorteners as pyst #used to shorten URLs
import pyperclip #to copy URL

st.set_page_config("Streamlit URL Shortener", layout = "wide")

st.markdown("<h1 style = 'text-align : center; color : lightblue;'>URL Shortener</h1>", unsafe_allow_html = True)
st.markdown("---")

def copy():
    pyperclip.copy(short_url)

form = st.form("Name")
url = form.text_input("URL Here")
submit = form.form_submit_button("Shorten URL")

shortener = pyst.Shortener()

if submit:
    short_url = shortener.tinyurl.short(url)
    st.markdown(f"<h4>Shortened URL : {short_url}</h4>", unsafe_allow_html = True)
    st.button("Copy", on_click = copy)
