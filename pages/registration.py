import streamlit as st

from database.mongodb import students_collection
st.title(":rainbow[---Student Registration----]")

first_name = st.text_input("First Name")

last_name = st.text_input("Last Name")

email = st.text_input(
    "Email"
)

course = st.text_input("Course")

if st.button("Register Student"):

    students_collection.insert_one({
      "first_name":first_name,
      "last_name" :last_name,
      "email":email, 
      "course": course
    })
    st.success("Student Registered Successfully!")