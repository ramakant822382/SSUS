import streamlit as st
import pandas as pd

from database.mongodb import students_collection

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Student List",
    page_icon="👨‍🎓",
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
    color:#1E3A8A;
}

.subtitle{
    color:aqua;
    font-size:18px;
}

.card{
    background:black;
    padding:18px;
    border-radius:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,.08);
    text-align:center;
}

.footer{
    text-align:center;
    color:gray;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Hero Section ----------------

left, right = st.columns([1.3,1])

with left:

    st.markdown(
        '<p class="title">👨‍🎓 Student List</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
<div class="subtitle">
Search, view and manage all registered students.
Find students quickly using their name or email.
</div>
""", unsafe_allow_html=True)

with right:

    st.image(
        "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=900",
        use_container_width=True
    )

st.divider()

# ---------------- Search ----------------

search = st.text_input(
    "🔍 Search Student (Name or Email)"
)

# -------- Query (UNCHANGED) --------

query = {}

if search:
    query = {
        "$or":[
            {
                "first_name":{
                    "$regex":search,
                    "$options":"i"
                }
            },
            {
                "email":{
                    "$regex":search,
                    "$options":"i"
                }
            }
        ]
    }

students = list(
    students_collection.find(query)
)

# ---------------- Dashboard ----------------

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown(f"""
<div class="card">
<h2>👨‍🎓</h2>
<h3>{len(students)}</h3>
Students Found
</div>
""", unsafe_allow_html=True)

with c2:

    courses = len(
        set(student["course"] for student in students)
    ) if students else 0

    st.markdown(f"""
<div class="card">
<h2>📚</h2>
<h3>{courses}</h3>
Courses
</div>
""", unsafe_allow_html=True)

with c3:

    emails = len(
        [student for student in students if student.get("email")]
    )

    st.markdown(f"""
<div class="card">
<h2>📧</h2>
<h3>{emails}</h3>
Emails
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- Student Table ----------------

st.subheader("📋 Registered Students")

if students:

    for student in students:
        student["_id"] = str(student["_id"])

    df = pd.DataFrame(students)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("No student found!")

st.divider()

# ---------------- Student Cards ----------------

if students:

    st.subheader("🎓 Student Cards")

    cols = st.columns(3)

    for index, student in enumerate(students):

        with cols[index % 3]:

            st.markdown(f"""
<div style="
background:black;
border:2px solid aqua;                        
padding:18px;
border-radius:15px;
box-shadow:0px 3px 10px rgba(0,0,0,.08);
margin-bottom:20px;
">

<h3>👨‍🎓 {student['first_name']} {student['last_name']}</h3>

<p><b>📧 Email</b><br>
{student['email']}</p>

<p><b>📚 Course</b><br>
{student['course']}</p>

</div>
""", unsafe_allow_html=True)

# ---------------- Footer ----------------

st.markdown("""
<hr>
<div class="footer">
© 2026 Student Utility System | Python • Streamlit • MongoDB
</div>
""", unsafe_allow_html=True)