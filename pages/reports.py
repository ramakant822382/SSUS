import pandas as pd 
import streamlit as st 

from database.mongodb import students_collection

data= list(
    students_collection.find()
)

df=pd.DataFrame(data)

st.dataframe(df)

st.bar_chart(
    df["first_name"]
)
