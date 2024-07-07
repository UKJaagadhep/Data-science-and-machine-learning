import streamlit as st
from PIL import Image
from PIL import ImageFilter

st.set_page_config("Streamlit Image Editor", layout = "wide")

st.markdown("<h1 style = 'text-align : center; color : lightblue;'>Image Editor</h1>", unsafe_allow_html = True)
st.markdown("---")

image = st.file_uploader("Upload your Image", type = ['jpeg', 'jpg', 'png'])
info = st.empty()
color_space = st.empty() 
file_type = st.empty()
shape = st.empty()

if image:
    img = Image.open(image)
    
    info.markdown("<h2 style = 'text-align : center;'>Image Info</h2>", unsafe_allow_html = True)  
    shape.markdown(f"<h6>Shape (i.e. size) : {img.size}</h6>", unsafe_allow_html = True)
    color_space.markdown(f"<h6>Color_space(i.e. mode) : {img.mode}</h6>", unsafe_allow_html = True)
    file_type.markdown(f"<h6>File Type (i.e. format) : {img.format}</h6>", unsafe_allow_html = True)
    
    st.markdown("<h2 style = 'text-align : center;'>Resizing</h2>", unsafe_allow_html = True)
    width = st.number_input("Enter width to resize to : ", value = img.width)
    height = st.number_input("Enter height tot resize to : ", value = img.height)

    st.markdown("<h2 style = 'text-align : center;'>Rotation</h2>", unsafe_allow_html = True)
    degree = st.number_input("Degree : ")

    st.markdown("<h2 style = 'text-align : center;'>Filters</h2>", unsafe_allow_html = True)
    filter = st.selectbox("Filter", options = ("None", "Blur", "Detail", "Emboss", "Smooth"))

    submit = st.button("Submit")

    if submit:
        edited_img = img.resize((width, height)).rotate(degree)
        
        if filter != "None":
            if filter == "Blur":
                edited_img = edited_img.filter(ImageFilter.BLUR)
            elif filter == "Detail":
                edited_img = edited_img.filter(ImageFilter.DETAIL)
            elif filter == "Emboss":
                edited_img = edited_img.filter(ImageFilter.EMBOSS)
            else:
                edited_img = edited_img.filter(ImageFilter.SMOOTH)
        st.image(edited_img)
                
