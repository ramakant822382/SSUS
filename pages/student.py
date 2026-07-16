import streamlit as st
import pandas as pd

from database.mongodb import students_collection

st.title("Student list")
search = st.text_input(
    "Search Student"
)
query = {}

if search:
    query={

        "$or":[
            {
                "first_name":{
                    "$regex":search,
                    "$options":"i"
                }
            },
            {
                "email":{
                   "$regex":search,
                   "$options":"i"
                }
            }
        ]
    }
    

students = list(students_collection.find(query))

if students:

    for student in students:
        student["_id"]=str(student["_id"])
    df = pd.DataFrame(students)
    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.warning("No student found!")