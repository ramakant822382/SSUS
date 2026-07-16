import streamlit as st
import pandas as pd

from database.mongodb import (
    students_collection,
    marks_collection
)

from utils.grade import calculate_grade

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Student Marks",
    page_icon="📚",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp{
    background:black;
}

.title{
    font-size:42px;
    font-weight:bold;
    color:#2E3A87;
}

.subtitle{
    color:aqua;
    font-size:18px;
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

# ---------------- Hero ----------------

left, right = st.columns([1.3,1])

with left:

    st.markdown(
        '<p class="title">📚 Student Marks Management</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
<div class="subtitle">
Manage student academic records by entering Python,
SQL and Excel marks. Automatically calculate
percentage and grade.
</div>
""", unsafe_allow_html=True)

with right:

    st.image(
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=900",
        use_container_width=True
    )

st.divider()

# ---------------- Students ----------------

students = list(
    students_collection.find()
)

if not students:
    st.warning("No students found")
    st.stop()

student_names = []

for student in students:

    full_name = (
        student["first_name"]
        + " "
        + student["last_name"]
    )

    student_names.append(full_name)

# ---------------- Dashboard ----------------

all_marks = list(
    marks_collection.find()
)

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown(f"""
<div class="card">
<h2>👨‍🎓</h2>
<h3>{len(student_names)}</h3>
Students
</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
<div class="card">
<h2>📄</h2>
<h3>{len(all_marks)}</h3>
Reports
</div>
""", unsafe_allow_html=True)

with c3:

    average = round(
        sum(i["percentage"] for i in all_marks)/len(all_marks),2
    ) if all_marks else 0

    st.markdown(f"""
<div class="card">
<h2>📊</h2>
<h3>{average}%</h3>
Average
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- Form ----------------

st.subheader("📝 Enter Student Marks")

col1,col2 = st.columns(2)

with col1:

    selected_student = st.selectbox(
        "👨‍🎓 Select Student",
        student_names
    )

    python_marks = st.number_input(
        "🐍 Python Marks",
        min_value=0,
        max_value=100
    )

with col2:

    sql_marks = st.number_input(
        "🗄 SQL Marks",
        min_value=0,
        max_value=100
    )

    excel_marks = st.number_input(
        "📗 Excel Marks",
        min_value=0,
        max_value=100
    )

save = st.button(
    "💾 Save Marks",
    use_container_width=True
)

# ---------------- Save ----------------

if save:

    percentage = (
        python_marks +
        sql_marks +
        excel_marks
    ) / 3

    grade = calculate_grade(
        percentage
    )

    # -------- MongoDB Query (UNCHANGED) --------

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
        round(percentage,2),

        "grade":
        grade

    })

    st.success("Marks Saved Successfully 🎉")

    r1,r2 = st.columns(2)

    with r1:
        st.metric(
            "Percentage",
            f"{round(percentage,2)}%"
        )

    with r2:

        if grade=="A":
            st.success(f"🏆 Grade : {grade}")

        elif grade=="B":
            st.info(f"📘 Grade : {grade}")

        elif grade=="C":
            st.warning(f"📙 Grade : {grade}")

        else:
            st.error(f"❌ Grade : {grade}")

st.divider()

# ---------------- Reports ----------------

st.subheader("📋 Student Marks Report")

all_marks = list(
    marks_collection.find()
)

if all_marks:

    data=[]

    for mark in all_marks:

        data.append({

            "Student":
            mark["student_name"],

            "Python":
            mark["python"],

            "SQL":
            mark["sql"],

            "Excel":
            mark["excel"],

            "Percentage":
            f'{mark["percentage"]}%',

            "Grade":
            mark["grade"]

        })

    df=pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No Marks Found")

st.divider()

# ---------------- Grade Summary ----------------

st.subheader("🏆 Grade Summary")

grades={}

for mark in all_marks:

    g=mark["grade"]

    grades[g]=grades.get(g,0)+1

if grades:

    cols = st.columns(len(grades))

    for i,(grade,count) in enumerate(grades.items()):

        with cols[i]:
            st.metric(
                f"Grade {grade}",
                count
            )

st.markdown("""
<hr>
<div class="footer">
© 2026 Student Utility System | Python • Streamlit • MongoDB
</div>
""", unsafe_allow_html=True)