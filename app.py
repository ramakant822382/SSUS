import streamlit as st
from datetime import datetime
import random

from database.mongodb import (
    students_collection,
    attendance_collection,
    marks_collection,
    bmi_collection
)

st.set_page_config(
    page_title="Student Utility",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Utility Dashboard")

st.write(f"📅 {datetime.now().strftime('%d %B %Y')}")

# ---------------- DATABASE DATA ----------------

total_students = students_collection.count_documents({})

total_attendance = attendance_collection.count_documents({})
present = attendance_collection.count_documents({"status": "Present"})

attendance_percent = (
    round((present / total_attendance) * 100, 2)
    if total_attendance > 0 else 0
)

total_marks = marks_collection.count_documents({})
total_bmi = bmi_collection.count_documents({})

# ---------------- DASHBOARD ----------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("👨‍🎓 Students", total_students)
c2.metric("📅 Attendance", f"{attendance_percent}%")
c3.metric("📚 Marks Reports", total_marks)
c4.metric("⚕️ BMI Reports", total_bmi)

st.divider()

# ---------------- RECENT STUDENTS ----------------

left, right = st.columns(2)

with left:

    st.subheader("👨‍🎓 Recent Students")

    students = list(
        students_collection.find().sort("_id", -1).limit(5)
    )

    if students:

        for s in students:

            st.write(
                f"• {s['first_name']} {s['last_name']} ({s['course']})"
            )

    else:
        st.info("No Students")

with right:

    st.subheader("📅 Recent Attendance")

    attendance = list(
        attendance_collection.find().sort("_id", -1).limit(5)
    )

    if attendance:

        for a in attendance:

            emoji = "✅" if a["status"] == "Present" else "❌"

            st.write(
                f"{emoji} {a['student_name']} - {a['date']}"
            )

    else:
        st.info("No Attendance")

st.divider()

# ---------------- TOP MARKS ----------------

left, right = st.columns(2)

with left:

    st.subheader("🏆 Top Students")

    top = list(
        marks_collection.find().sort("percentage", -1).limit(5)
    )

    if top:

        for i in top:

            st.write(
                f"🥇 {i['student_name']} - {i['percentage']}% ({i['grade']})"
            )

    else:
        st.info("No Marks Data")

with right:

    st.subheader("⚕️ Latest BMI")

    bmi = list(
        bmi_collection.find().sort("_id", -1).limit(5)
    )

    if bmi:

        for b in bmi:

            st.write(
                f"👤 {b['student_name']} | BMI : {b['bmi']} ({b['category']})"
            )

    else:
        st.info("No BMI Data")

st.divider()

# ---------------- STUDY TIP ----------------

tips = [
    "📘 Revise your notes every day.",
    "💻 Practice coding regularly.",
    "📝 Complete assignments on time.",
    "📖 Read for at least 1 hour daily.",
    "🎯 Focus on one subject at a time."
]

st.success(random.choice(tips))

st.divider()

# ---------------- FOOTER ----------------

st.caption("Made with ❤️ using Streamlit")