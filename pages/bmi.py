import streamlit as st
import pandas as pd

from database.mongodb import students_collection, bmi_collection

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚕️",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp{
    background-color:black;
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
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Hero Section ----------------

left, right = st.columns([1.3,1])

with left:

    st.markdown('<p class="title">⚕️ BMI Calculator</p>', unsafe_allow_html=True)

    st.markdown("""
<div class="subtitle">
Calculate and monitor students' Body Mass Index (BMI).
Store reports securely and view health summaries.
</div>
""", unsafe_allow_html=True)

with right:

    st.image(
        "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=900",
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

reports = list(bmi_collection.find())

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
    st.markdown(f"""
<div class="card">
<h2>📄</h2>
<h3>{len(reports)}</h3>
BMI Reports
</div>
""", unsafe_allow_html=True)

with c3:
    average = round(
        sum(r["bmi"] for r in reports)/len(reports),2
    ) if reports else 0

    st.markdown(f"""
<div class="card">
<h2>⚕️</h2>
<h3>{average}</h3>
Average BMI
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- BMI Form ----------------

st.subheader("📝 Calculate BMI")

col1, col2 = st.columns(2)

with col1:

    selected_student = st.selectbox(
        "👨‍🎓 Select Student",
        student_names
    )

    height = st.number_input(
        "📏 Height (meters)",
        min_value=0.5,
        max_value=3.0,
        value=1.70,
        step=0.01
    )

with col2:

    weight = st.number_input(
        "⚖️ Weight (kilograms)",
        min_value=1.0,
        max_value=300.0,
        value=70.0,
        step=0.1
    )

    st.write("")
    st.write("")

    calculate = st.button(
        "⚕️ Calculate BMI",
        use_container_width=True
    )

# ---------------- Calculate BMI ----------------

if calculate:

    bmi = round(weight / (height ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"

    elif bmi < 25:
        category = "Normal weight"

    elif bmi < 30:
        category = "Overweight"

    else:
        category = "Obesity"

    st.metric("BMI Score", bmi)

    if category == "Normal weight":
        st.success(f"✅ Category : {category}")

    elif category == "Underweight":
        st.warning(f"⚠️ Category : {category}")

    else:
        st.error(f"🚨 Category : {category}")

    # ---------------- MongoDB Query (Unchanged) ----------------

    bmi_collection.insert_one({
        "student_name": selected_student,
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "category": category
    })

    st.success("BMI Report Saved Successfully!")

st.divider()

# ---------------- Reports ----------------

st.subheader("📋 BMI Reports")

reports = list(bmi_collection.find())

if reports:

    data=[]

    for report in reports:

        data.append({
            "Student":report["student_name"],
            "Height (m)":report["height"],
            "Weight (kg)":report["weight"],
            "BMI":report["bmi"],
            "Category":report["category"]
        })

    df=pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("No BMI Reports Found.")

st.divider()

# ---------------- Summary ----------------

st.subheader("📊 BMI Summary")

st.metric(
    "Total BMI Reports",
    len(reports)
)

if reports:

    categories={}

    for report in reports:

        cat=report["category"]

        categories[cat]=categories.get(cat,0)+1

    for key,value in categories.items():

        st.write(f"**{key}**")

        st.progress(value/len(reports))

        st.caption(f"{value} Student(s)")

# ---------------- Footer ----------------

st.markdown("""
<hr>
<div class="footer">
© 2026 Student Utility System | Python • Streamlit • MongoDB
</div>
""", unsafe_allow_html=True)