import streamlit as st
import pandas as pd

from database.mongodb import (
    students_collection,
    attendance_collection
)

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Attendance Management",
    page_icon="📅",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp{
    background-color:black;
}

.main-title{
    font-size:45px;
    font-weight:bold;
    color:#1E3A8A;
}

.sub-text{
    font-size:18px;
    color:aqua;
}

.card{
    background:black;
    padding:18px;
    border-radius:15px;
    box-shadow:0px 3px 12px rgba(0,0,0,.08);
    text-align:center;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Hero Section ----------------

left, right = st.columns([1.3,1])

with left:

    st.markdown('<p class="main-title">📅 Attendance Management</p>',
                unsafe_allow_html=True)

    st.markdown("""
    <p class="sub-text">
    Manage student attendance quickly and efficiently.
    Record attendance, monitor performance and generate attendance summaries.
    </p>
    """, unsafe_allow_html=True)

with right:

    st.image(
        "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=900",
        use_container_width=True
    )

st.divider()

# ---------------- Load Students ----------------

students = list(students_collection.find())

if not students:
    st.warning("No students found. Please register students first.")
    st.stop()

student_names = []

for student in students:
    full_name = student["first_name"] + " " + student["last_name"]
    student_names.append(full_name)

# ---------------- Dashboard ----------------

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card">
    <h2>👨‍🎓</h2>
    <h3>{len(student_names)}</h3>
    Students
    </div>
    """, unsafe_allow_html=True)

with c2:
    total_records = attendance_collection.count_documents({})
    st.markdown(f"""
    <div class="card">
    <h2>📅</h2>
    <h3>{total_records}</h3>
    Attendance Records
    </div>
    """, unsafe_allow_html=True)

with c3:
    total_present = attendance_collection.count_documents({"status":"Present"})
    st.markdown(f"""
    <div class="card">
    <h2>✅</h2>
    <h3>{total_present}</h3>
    Present Records
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- Attendance Form ----------------

st.subheader("📝 Mark Attendance")

col1, col2 = st.columns(2)

with col1:

    selected_student = st.selectbox(
        "👨‍🎓 Select Student",
        student_names
    )

    attendance_date = st.date_input(
        "📅 Attendance Date"
    )

with col2:

    status = st.selectbox(
        "✅ Attendance Status",
        ["Present","Absent"]
    )

    st.write("")
    st.write("")

    mark = st.button(
        "✔ Mark Attendance",
        use_container_width=True
    )

if mark:

    attendance_collection.insert_one({
        "student_name": selected_student,
        "date": str(attendance_date),
        "status": status
    })

    st.success("Attendance marked successfully!")

st.divider()

# ---------------- Attendance Records ----------------

st.subheader("📋 Attendance Records")

records = list(attendance_collection.find())

if records:

    data = []

    for record in records:

        data.append({
            "Student": record["student_name"],
            "Date": record["date"],
            "Status": record["status"]
        })

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No attendance records found.")

st.divider()

# ---------------- Attendance Summary ----------------

st.subheader("📊 Attendance Summary")

for student in student_names:

    total = attendance_collection.count_documents({
        "student_name": student
    })

    present = attendance_collection.count_documents({
        "student_name": student,
        "status": "Present"
    })

    if total > 0:

        percentage = (present / total) * 100

        st.write(f"**{student}**")

        st.progress(percentage / 100)

        st.write(f"Attendance : **{round(percentage,2)}%**")

        st.write("")

# ---------------- Footer ----------------

st.markdown("""
<hr>
<div class="footer">
© 2026 Student Utility System | Developed using Python, Streamlit & MongoDB
</div>
""", unsafe_allow_html=True)