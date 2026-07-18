import streamlit as st
import pandas as pd
from datetime import date, datetime

from database.mongodb import (
    students_collection,
    attendance_collection
)

st.set_page_config(
    page_title="Attendance Management",
    page_icon="📅",
    layout="wide"
)

st.title("📅 Attendance Management")

# ---------------- Load Students ----------------

students = list(students_collection.find())

if not students:
    st.warning("No students found.")
    st.stop()

student_names = [
    f"{s['first_name']} {s['last_name']}"
    for s in students
]

# ---------------- Dashboard ----------------

col1, col2, col3 = st.columns(3)

col1.metric("Students", len(student_names))
col2.metric(
    "Attendance",
    attendance_collection.count_documents({})
)
col3.metric(
    "Present",
    attendance_collection.count_documents(
        {"status": "Present"}
    )
)

st.divider()

# ===================================================
# CREATE
# ===================================================

st.subheader("➕ Add Attendance")

c1, c2, c3 = st.columns(3)

with c1:
    student = st.selectbox(
        "Student",
        student_names,
        key="add_student"
    )

with c2:
    attendance_date = st.date_input(
        "Date",
        value=date.today(),
        key="add_date"
    )

with c3:
    status = st.selectbox(
        "Status",
        ["Present", "Absent"],
        key="add_status"
    )

if st.button("Save Attendance"):

    attendance_collection.insert_one({
        "student_name": student,
        "date": str(attendance_date),
        "status": status
    })

    st.success("Attendance Added Successfully")
    st.rerun()

st.divider()

# ===================================================
# READ
# ===================================================

st.subheader("📋 Attendance Records")

records = list(attendance_collection.find())

if records:

    table = []

    for record in records:

        table.append({
            "_id": str(record["_id"]),
            "Student": record["student_name"],
            "Date": record["date"],
            "Status": record["status"]
        })

    df = pd.DataFrame(table)

    st.dataframe(
        df.drop(columns="_id"),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ===================================================
    # UPDATE & DELETE
    # ===================================================

    st.subheader("✏ Update / Delete Attendance")

    selected_id = st.selectbox(
        "Select Record",
        df["_id"],
        format_func=lambda x:
            df[df["_id"] == x]["Student"].iloc[0]
            + " | "
            + df[df["_id"] == x]["Date"].iloc[0],
        key="record_select"
    )

    selected_record = None

    for record in records:
        if str(record["_id"]) == selected_id:
            selected_record = record
            break

    c1, c2, c3 = st.columns(3)

    with c1:

        edit_student = st.selectbox(
            "Student",
            student_names,
            index=student_names.index(
                selected_record["student_name"]
            ),
            key="edit_student"
        )

    with c2:

        edit_date = st.date_input(
            "Date",
            value=datetime.strptime(
                selected_record["date"],
                "%Y-%m-%d"
            ),
            key="edit_date"
        )

    with c3:

        edit_status = st.selectbox(
            "Status",
            ["Present", "Absent"],
            index=0 if selected_record["status"] == "Present" else 1,
            key="edit_status"
        )

    b1, b2 = st.columns(2)

    with b1:

        if st.button("Update Attendance"):

            attendance_collection.update_one(
                {"_id": selected_record["_id"]},
                {
                    "$set": {
                        "student_name": edit_student,
                        "date": str(edit_date),
                        "status": edit_status
                    }
                }
            )

            st.success("Attendance Updated")
            st.rerun()

    with b2:

        if st.button("Delete Attendance"):

            attendance_collection.delete_one(
                {"_id": selected_record["_id"]}
            )

            st.success("Attendance Deleted")
            st.rerun()

else:

    st.info("No Attendance Records Found.")

st.divider()

# ===================================================
# SUMMARY
# ===================================================

st.subheader("📊 Attendance Summary")

for student in student_names:

    total = attendance_collection.count_documents(
        {"student_name": student}
    )

    present = attendance_collection.count_documents(
        {
            "student_name": student,
            "status": "Present"
        }
    )

    if total > 0:

        percentage = round(
            (present / total) * 100,
            2
        )

        st.write(f"**{student}**")

        st.progress(percentage / 100)

        st.write(f"{percentage}% Attendance")