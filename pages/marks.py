import streamlit as st
import pandas as pd

from database.mongodb import (
    students_collection,
    marks_collection
)

from utils.grade import calculate_grade

st.set_page_config(
    page_title="Student Marks",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Student Marks Management")

# ---------------- Students ----------------

students = list(students_collection.find())

if not students:
    st.warning("No students found.")
    st.stop()

student_names = [
    f"{s['first_name']} {s['last_name']}"
    for s in students
]

# ---------------- Dashboard ----------------

records = list(marks_collection.find())

c1, c2, c3 = st.columns(3)

c1.metric("Students", len(student_names))
c2.metric("Reports", len(records))

avg = round(
    sum(r["percentage"] for r in records) / len(records),
    2
) if records else 0

c3.metric("Average %", avg)

st.divider()

# ====================================================
# CREATE
# ====================================================

st.subheader("➕ Add Marks")

col1, col2 = st.columns(2)

with col1:

    student = st.selectbox(
        "Student",
        student_names,
        key="add_student"
    )

    python_marks = st.number_input(
        "Python",
        0,
        100,
        key="add_python"
    )

with col2:

    sql_marks = st.number_input(
        "SQL",
        0,
        100,
        key="add_sql"
    )

    excel_marks = st.number_input(
        "Excel",
        0,
        100,
        key="add_excel"
    )

if st.button("Save Marks"):

    percentage = round(
        (python_marks + sql_marks + excel_marks) / 3,
        2
    )

    grade = calculate_grade(percentage)

    marks_collection.insert_one({

        "student_name": student,
        "python": python_marks,
        "sql": sql_marks,
        "excel": excel_marks,
        "percentage": percentage,
        "grade": grade

    })

    st.success("Marks Saved Successfully")
    st.rerun()

st.divider()

# ====================================================
# READ
# ====================================================

st.subheader("📋 Marks Records")

records = list(marks_collection.find())

if records:

    table = []

    for record in records:

        table.append({

            "_id": str(record["_id"]),
            "Student": record["student_name"],
            "Python": record["python"],
            "SQL": record["sql"],
            "Excel": record["excel"],
            "Percentage": record["percentage"],
            "Grade": record["grade"]

        })

    df = pd.DataFrame(table)

    st.dataframe(
        df.drop(columns="_id"),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ====================================================
    # UPDATE & DELETE
    # ====================================================

    st.subheader("✏ Update / Delete Marks")

    selected_id = st.selectbox(

        "Select Record",

        df["_id"],

        format_func=lambda x:
            df[df["_id"] == x]["Student"].iloc[0],

        key="record_select"

    )

    selected = None

    for record in records:

        if str(record["_id"]) == selected_id:
            selected = record
            break

    c1, c2 = st.columns(2)

    with c1:

        edit_student = st.selectbox(

            "Student",

            student_names,

            index=student_names.index(
                selected["student_name"]
            ),

            key="edit_student"

        )

        edit_python = st.number_input(

            "Python",

            0,
            100,

            value=int(selected["python"]),

            key="edit_python"

        )

    with c2:

        edit_sql = st.number_input(

            "SQL",

            0,
            100,

            value=int(selected["sql"]),

            key="edit_sql"

        )

        edit_excel = st.number_input(

            "Excel",

            0,
            100,

            value=int(selected["excel"]),

            key="edit_excel"

        )

    percentage = round(
        (edit_python + edit_sql + edit_excel) / 3,
        2
    )

    grade = calculate_grade(percentage)

    b1, b2 = st.columns(2)

    with b1:

        if st.button("Update"):

            marks_collection.update_one(

                {"_id": selected["_id"]},

                {
                    "$set": {

                        "student_name": edit_student,
                        "python": edit_python,
                        "sql": edit_sql,
                        "excel": edit_excel,
                        "percentage": percentage,
                        "grade": grade

                    }
                }

            )

            st.success("Updated Successfully")
            st.rerun()

    with b2:

        if st.button("Delete"):

            marks_collection.delete_one(
                {"_id": selected["_id"]}
            )

            st.success("Deleted Successfully")
            st.rerun()

else:

    st.info("No Marks Found")

st.divider()

# ====================================================
# SUMMARY
# ====================================================

st.subheader("📊 Grade Summary")

grade_count = {}

for record in records:

    g = record["grade"]

    grade_count[g] = grade_count.get(g, 0) + 1

if grade_count:

    cols = st.columns(len(grade_count))

    for i, (g, count) in enumerate(grade_count.items()):

        cols[i].metric(
            f"Grade {g}",
            count
        )