import streamlit as st
import pandas as pd

from database.mongodb import students_collection

st.set_page_config(
    page_title="Students",
    page_icon="👨‍🎓",
    layout="wide"
)

st.title("👨‍🎓 Student Management")

# ====================================================
# SEARCH
# ====================================================

search = st.text_input("🔍 Search Student")

query = {}

if search:
    query = {
        "$or": [
            {
                "first_name": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "email": {
                    "$regex": search,
                    "$options": "i"
                }
            }
        ]
    }

students = list(students_collection.find(query))

# ====================================================
# DASHBOARD
# ====================================================

c1, c2, c3 = st.columns(3)

c1.metric("Students", len(students))

courses = len(
    set(s["course"] for s in students)
) if students else 0

c2.metric("Courses", courses)

emails = len(
    [s for s in students if s.get("email")]
)

c3.metric("Emails", emails)

st.divider()

# ====================================================
# CREATE
# ====================================================

st.subheader("➕ Add Student")

col1, col2 = st.columns(2)

with col1:

    first_name = st.text_input(
        "First Name",
        key="first_name"
    )

    email = st.text_input(
        "Email",
        key="email"
    )

with col2:

    last_name = st.text_input(
        "Last Name",
        key="last_name"
    )

    course = st.text_input(
        "Course",
        key="course"
    )

if st.button("Save Student"):

    students_collection.insert_one({

        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "course": course

    })

    st.success("Student Added Successfully")
    st.rerun()

st.divider()

# ====================================================
# READ
# ====================================================

st.subheader("📋 Student List")

students = list(students_collection.find(query))

if students:

    data = []

    for student in students:

        data.append({

            "_id": str(student["_id"]),
            "First Name": student["first_name"],
            "Last Name": student["last_name"],
            "Email": student["email"],
            "Course": student["course"]

        })

    df = pd.DataFrame(data)

    st.dataframe(
        df.drop(columns="_id"),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ====================================================
    # UPDATE & DELETE
    # ====================================================

    st.subheader("✏ Update / Delete Student")

    selected_id = st.selectbox(

        "Select Student",

        df["_id"],

        format_func=lambda x:
            df[df["_id"] == x]["First Name"].iloc[0]
            + " "
            + df[df["_id"] == x]["Last Name"].iloc[0],

        key="student_select"

    )

    selected = None

    for student in students:

        if str(student["_id"]) == selected_id:
            selected = student
            break

    col1, col2 = st.columns(2)

    with col1:

        edit_first = st.text_input(
            "First Name",
            value=selected["first_name"],
            key="edit_first"
        )

        edit_email = st.text_input(
            "Email",
            value=selected["email"],
            key="edit_email"
        )

    with col2:

        edit_last = st.text_input(
            "Last Name",
            value=selected["last_name"],
            key="edit_last"
        )

        edit_course = st.text_input(
            "Course",
            value=selected["course"],
            key="edit_course"
        )

    b1, b2 = st.columns(2)

    with b1:

        if st.button("Update Student"):

            students_collection.update_one(

                {"_id": selected["_id"]},

                {
                    "$set": {

                        "first_name": edit_first,
                        "last_name": edit_last,
                        "email": edit_email,
                        "course": edit_course

                    }
                }

            )

            st.success("Student Updated Successfully")
            st.rerun()

    with b2:

        if st.button("Delete Student"):

            students_collection.delete_one(
                {"_id": selected["_id"]}
            )

            st.success("Student Deleted Successfully")
            st.rerun()

else:

    st.warning("No Student Found")