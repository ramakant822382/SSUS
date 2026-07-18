import streamlit as st
import pandas as pd

from database.mongodb import (
    students_collection,
    bmi_collection
)

st.set_page_config(
    page_title="BMI Management",
    page_icon="⚕️",
    layout="wide"
)

st.title("⚕️ BMI Calculator")

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

reports = list(bmi_collection.find())

c1, c2, c3 = st.columns(3)

c1.metric("Students", len(student_names))
c2.metric("BMI Reports", len(reports))

avg = round(
    sum(r["bmi"] for r in reports) / len(reports),
    2
) if reports else 0

c3.metric("Average BMI", avg)

st.divider()

# =====================================================
# CREATE
# =====================================================

st.subheader("➕ Add BMI Report")

col1, col2, col3 = st.columns(3)

with col1:
    student = st.selectbox(
        "Student",
        student_names,
        key="add_student"
    )

with col2:
    height = st.number_input(
        "Height (m)",
        min_value=0.5,
        max_value=3.0,
        value=1.70,
        step=0.01,
        key="add_height"
    )

with col3:
    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=300.0,
        value=70.0,
        step=0.1,
        key="add_weight"
    )

if st.button("Save BMI"):

    bmi = round(weight / (height ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obesity"

    bmi_collection.insert_one({
        "student_name": student,
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "category": category
    })

    st.success("BMI Saved Successfully")
    st.rerun()

st.divider()

# =====================================================
# READ
# =====================================================

st.subheader("📋 BMI Reports")

reports = list(bmi_collection.find())

if reports:

    table = []

    for report in reports:

        table.append({
            "_id": str(report["_id"]),
            "Student": report["student_name"],
            "Height": report["height"],
            "Weight": report["weight"],
            "BMI": report["bmi"],
            "Category": report["category"]
        })

    df = pd.DataFrame(table)

    st.dataframe(
        df.drop(columns="_id"),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =====================================================
    # UPDATE & DELETE
    # =====================================================

    st.subheader("✏ Update / Delete BMI")

    selected_id = st.selectbox(
        "Select Report",
        df["_id"],
        format_func=lambda x:
            df[df["_id"] == x]["Student"].iloc[0],
        key="select_report"
    )

    selected = None

    for report in reports:
        if str(report["_id"]) == selected_id:
            selected = report
            break

    c1, c2, c3 = st.columns(3)

    with c1:

        edit_student = st.selectbox(
            "Student",
            student_names,
            index=student_names.index(
                selected["student_name"]
            ),
            key="edit_student"
        )

    with c2:

        edit_height = st.number_input(
            "Height",
            value=float(selected["height"]),
            key="edit_height"
        )

    with c3:

        edit_weight = st.number_input(
            "Weight",
            value=float(selected["weight"]),
            key="edit_weight"
        )

    bmi = round(edit_weight / (edit_height ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obesity"

    b1, b2 = st.columns(2)

    with b1:

        if st.button("Update BMI"):

            bmi_collection.update_one(
                {"_id": selected["_id"]},
                {
                    "$set": {
                        "student_name": edit_student,
                        "height": edit_height,
                        "weight": edit_weight,
                        "bmi": bmi,
                        "category": category
                    }
                }
            )

            st.success("BMI Updated Successfully")
            st.rerun()

    with b2:

        if st.button("Delete BMI"):

            bmi_collection.delete_one(
                {"_id": selected["_id"]}
            )

            st.success("BMI Deleted Successfully")
            st.rerun()

else:

    st.info("No BMI Reports Found.")

st.divider()

# =====================================================
# SUMMARY
# =====================================================

st.subheader("📊 BMI Summary")

for student in student_names:

    report = bmi_collection.find_one(
        {"student_name": student},
        sort=[("_id", -1)]
    )

    if report:

        st.write(
            f"**{student}** : "
            f"BMI **{report['bmi']}** "
            f"({report['category']})"
        )