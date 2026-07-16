import streamlit as st
from datetime import datetime
import random

st.set_page_config(
    page_title="Student Utility",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.main{
    background: linear-gradient(to right,#eef2ff,#f8fbff);
}

.hero{
    background: linear-gradient(135deg,#4F46E5,#06B6D4);
    padding:35px;
    border-radius:18px;
    text-align:center;
    color:white;
    margin-bottom:25px;
}

.hero h1{
    font-size:48px;
}

.card{
    background:black;
    color:aqua;        
    padding:25px;
    border-radius:18px;
    text-align:center;
    box-shadow:0px 5px 18px rgba(0,0,0,.1);
    transition:0.3s;
}

.card:hover{
    transform:translateY(-8px);
    box-shadow:0px 12px 25px rgba(0,0,0,.2);
}

.stat{
    background:black;
    color:aqua;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0 2px 10px rgba(0,0,0,.08);
}

.tip{
    background: linear-gradient(135deg,#4F46E5,#06B6D4);
    padding:18px;
    border-radius:12px;
    border-left:6px solid #0284C7;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Hero ---------------- #

st.markdown("""
<div class="hero">
<h1>🎓 Student Utility</h1>
<h4>Everything a Student Needs in One Place</h4>
</div>
""", unsafe_allow_html=True)

# ---------------- Date ---------------- #

today = datetime.now()

st.info(f"📅 {today.strftime('%A, %d %B %Y')}")

# ---------------- Statistics ---------------- #

s1,s2,s3,s4=st.columns(4)

with s1:
    st.markdown("""
    <div class="stat">
    <h2>25</h2>
    <p>Subjects</p>
    </div>
    """,unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="stat">
    <h2>90%</h2>
    <p>Attendance</p>
    </div>
    """,unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="stat">
    <h2>12</h2>
    <p>Assignments</p>
    </div>
    """,unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class="stat">
    <h2>5</h2>
    <p>Exams</p>
    </div>
    """,unsafe_allow_html=True)

st.write("")

# ---------------- Feature Cards ---------------- #

col1,col2,col3,col4=st.columns(4)

cards=[
("📚","Notes","Organize study materials"),
("📅","Attendance","Track attendance easily"),
("📝","Assignments","Never miss deadlines"),
("🧮","Calculator","Quick calculations")
]

for col,(icon,title,desc) in zip([col1,col2,col3,col4],cards):
    with col:
        st.markdown(f"""
        <div class="card">
        <h1>{icon}</h1>
        <h3>{title}</h3>
        <p>{desc}</p>
        </div>
        """,unsafe_allow_html=True)

st.write("")

# ---------------- Progress ---------------- #

st.subheader("🎯 Semester Progress")

st.progress(68)

st.caption("68% Semester Completed")

st.write("")

# ---------------- Study Tip ---------------- #

tips=[
"Revise your notes before sleeping.",
"Study 45 minutes then take a 10 minute break.",
"Practice coding daily.",
"Complete assignments before deadlines.",
"Make short notes for revision."
]

st.markdown(f"""
<div class="tip">
<h4>💡 Daily Study Tip</h4>
<p>{random.choice(tips)}</p>
</div>
""",unsafe_allow_html=True)

st.write("")

# ---------------- Announcement ---------------- #

st.success("📢 Mid Semester Exams start from next Monday.")

st.write("")

# ---------------- Quick Access ---------------- #

st.subheader("🚀 Quick Access")

c1,c2,c3,c4=st.columns(4)

with c1:
    st.button("📖 Open Notes",use_container_width=True)

with c2:
    st.button("📅 Attendance",use_container_width=True)

with c3:
    st.button("📝 Assignments",use_container_width=True)

with c4:
    st.button("🧮 Calculator",use_container_width=True)

st.write("")

# ---------------- Footer ---------------- #

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")