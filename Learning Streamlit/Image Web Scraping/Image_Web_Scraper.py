import streamlit as st
import requests
from bs4 import BeautifulSoup
import webbrowser

st.set_page_config(page_title = "Image Web Scraping", layout = "wide",
                   #menu_items = links_of_menu_items_in_a_dictionary
                   )

st.markdown("<h1 style = 'text-align : center; color : lightblue'> Image Web Scraper</h>", unsafe_allow_html = True)
with st.form("Search"):
    search = st.text_input("Search")
    submit = st.form_submit_button("Submit")
    
placeholder = st.empty()
if search: 
    website_url = f"https://unsplash.com/s/photos/{search}"
    #print(website_url)
    page = requests.get(website_url)
    #print(page.status_code) #to check if connection was successful or not
    soup = BeautifulSoup(page.content, features="lxml")
    columns = soup.find_all("div", class_ = "d95fI")
    #print(len(columns))
    col1, col2 = placeholder.columns(2) #We should create empty placeholder only after getting our requests
    for index, column in enumerate(columns):
        figures = column.find_all("figure")
        for j in range(2):
            img = figures[j].find_all("img")
            for i in img:
                if i.has_attr('srcset'):
                    #print(i["srcset"])
                    srcset = i['srcset']
                    if srcset:
                        list = srcset.split("?")[0]
                        anchor = figures[j].find("a", class_ = "Prxeh")
                        #print(anchor["href"]) #For download link
                        if j == 0:
                            col1.image(list)
                            key = str(index) + str(j) + str(i)
                            btn = col1.button("Download", key = key) #Each button widget must have a unique key
                            if btn:
                                webbrowser.open_new_tab("https://unsplash.com" + anchor["href"])
                        else:
                            col2.image(list)
                            key = str(index) + str(j) + str(i)
                            btn = col2.button("Download", key = key)
                            if btn:
                                webbrowser.open_new_tab("https://unsplash.com" + anchor["href"])
                        
        

