import streamlit as st

st.markdown("<h1>User Registration Form</h1>", unsafe_allow_html = True)
form = st.form("form")
name = form.text_input("Name")
roll = form.text_input("Roll Number")
department = form.selectbox("Department", options = ("AIE", "CSE", "CYS", "ARE", "ECE", "CCE"))
section = form.selectbox("Section", options = ("A", "B"))
interests = form.multiselect("Interested Domain", options = ("AI/ML", "Cybersecurity", "Competitive Programming",
                                                            "Web Development", "Blockchain", "Cloud Computing", "DevOps"))
form.form_submit_button("Submit")

user_details = {
    "name" : name,
    "roll_no" : roll,
    "department" : department,
    "section" : section,
    "interests" : interests
    }
print(user_details)
