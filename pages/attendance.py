import streamlit as st

from database.mongodb import (
    students_collection,
    attendance_collection
)

st.title("Attendance Management")

students = list(students_collection.find())

if not students:
    st.warning("No students found. Please register students first.")

    st.stop()

student_names = []
for student in students:
    full_name = (student["first_name"] + " " + student["last_name"])
    student_names.append(full_name)

selected_student = st.selectbox("Select a student", student_names)

attendance_date = st.date_input("Attendance Date")

status = st.selectbox("Attendance Status", ["Present", "Absent"])

if st.button("Mark Attendance"):

    attendance_collection.insert_one({"student_name": selected_student, "date": str(attendance_date), "status": status})
    st.success("Attendance marked successfully!")

    st.subheader("Attendance Records")

    records = list(attendance_collection.find())

    for record in records:
        st.write(record["student_name"], "|", record["date"], "|", record["status"])

st.subheader("Attendance Summary")

for student in student_names:
    
    total = attendance_collection.count_documents({"student_name": student})
    present = attendance_collection.count_documents({"student_name": student, "status": "Present"})

    if total > 0:
        percentage = (present / total) * 100

        st.write(f"{student}:"f"{round(percentage, 2)}%")