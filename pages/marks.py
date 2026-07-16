import streamlit as st

from database.mongodb import (
    students_collection,
    marks_collection
)

from utils.grade import calculate_grade

st.title("Marks Management")

students = list(
    students_collection.find()
)

if not students:
    st.warning(
        "No students found"
    )

    st.stop()

student_names = []

for student in students:

    full_name = (
        student["first_name"]
        + " "
        + student["last_name"]
    )

    student_names.append(full_name)

selected_student = st.selectbox(
    "Select Student",
    student_names
)

python_marks = st.number_input(
    "Python Marks",
    min_value=0,
    max_value=100
)

sql_marks = st.number_input(
    "SQL Marks",
    min_value=0,
    max_value=100
)

excel_marks = st.number_input(
    "Excel Marks",
    min_value=0,
    max_value=100
)

if st.button("Save Marks"):

    percentage = (
        python_marks +
        sql_marks +
        excel_marks
    ) / 3

    grade = calculate_grade(
        percentage
    )

    marks_collection.insert_one({

        "student_name":
        selected_student,

        "python":
        python_marks,

        "sql":
        sql_marks,

        "excel":
        excel_marks,

        "percentage":
        round(percentage, 2),

        "grade":
        grade

    })

    st.success(
        "Marks Saved Successfully"
    )

    st.write(
        "Percentage:",
        round(percentage, 2)
    )

    st.write(
        "Grade:",
        grade
    )

st.subheader("All Marks")

all_marks = list(
    marks_collection.find()
)

for mark in all_marks:

    st.write(
        f"{mark['student_name']} | "
        f"{mark['percentage']}% | "
        f"{mark['grade']}"
    )