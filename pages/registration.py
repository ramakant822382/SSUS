import streamlit as st
from database.mongodb import students_collection

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Student Registration",
    page_icon="🎓",
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
    font-size:18px;
    color:aqua;
}

.card{
    background:black;
    padding:20px;
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

    st.markdown(
        '<p class="title">🎓 Student Registration</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
<div class="subtitle">
Register new students easily by entering their
basic information. All records are securely
stored in the database.
</div>
""", unsafe_allow_html=True)

with right:

    st.image(
        "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=900",
        use_container_width=True
    )

st.divider()

# ---------------- Dashboard ----------------

students = list(students_collection.find())

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
<div class="card">
<h2>👨‍🎓</h2>
<h3>{len(students)}</h3>
Registered Students
</div>
""", unsafe_allow_html=True)

with c2:
    courses = len(set(student["course"] for student in students)) if students else 0

    st.markdown(f"""
<div class="card">
<h2>📚</h2>
<h3>{courses}</h3>
Courses
</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown("""
<div class="card">
<h2>📝</h2>
<h3>New</h3>
Registration
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- Registration Form ----------------

st.subheader("📝 Register Student")

col1, col2 = st.columns(2)

with col1:

    first_name = st.text_input(
        "👤 First Name"
    )

    email = st.text_input(
        "📧 Email"
    )

with col2:

    last_name = st.text_input(
        "👤 Last Name"
    )

    course = st.text_input(
        "📚 Course"
    )

st.write("")

register = st.button(
    "🎓 Register Student",
    use_container_width=True
)

# ---------------- Save ----------------

if register:

    if first_name and last_name and email and course:

        # -------- MongoDB Query (UNCHANGED) --------

        students_collection.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "course": course
        })

        st.success("🎉 Student Registered Successfully!")

        st.balloons()

        st.info(f"""
**Student Details**

👤 Name : {first_name} {last_name}

📧 Email : {email}

📚 Course : {course}
""")

    else:
        st.warning("Please fill all fields.")

st.divider()

# ---------------- Recently Registered Students ----------------

st.subheader("👨‍🎓 Registered Students")

if students:

    import pandas as pd

    data = []

    for student in students:

        data.append({
            "First Name": student["first_name"],
            "Last Name": student["last_name"],
            "Email": student["email"],
            "Course": student["course"]
        })

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No students registered yet.")

# ---------------- Footer ----------------

st.markdown("""
<hr>
<div class="footer">
© 2026 Student Utility System | Python • Streamlit • MongoDB
</div>
""", unsafe_allow_html=True)