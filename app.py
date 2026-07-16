import streamlit as st
st.set_page_config(page_title="Student Utility", layout="wide")

st.markdown("""
<style>

/* Hide Streamlit default menu */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Hero Section */
.hero{
    background-image:url('https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1600&q=80');
    background-size:cover;
    background-position:center;
    border-radius:20px;
    height:520px;
    display:flex;
    align-items:center;
    justify-content:center;
}

.overlay{
    background:rgba(0,0,0,.55);
    padding:60px;
    border-radius:20px;
    text-align:center;
}

.title{
    color:white;
    font-size:58px;
    font-weight:700;
}

.subtitle{
    color:white;
    font-size:22px;
}

/* Feature Cards */
.card{
    background:black;
    padding:25px;
    border-radius:18px;
    text-align:center;
    box-shadow:0 10px 25px rgba(0,0,0,.15);
    transition:.3s;
}

.card:hover{
    transform:translateY(-8px);
}

.icon{
    font-size:50px;
}

</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="overlay">
        <div class="title">🎓 Student Utility Portal</div>
        <br>
        <div class="subtitle">
        Everything a student needs in one place.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

col1,col2,col3,col4=st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
    <div class="icon">📚</div>
    <h3>Notes</h3>
    Organize study materials.
    </div>
    """,unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <div class="icon">📅</div>
    <h3>Attendance</h3>
    Track attendance easily.
    </div>
    """,unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <div class="icon">📝</div>
    <h3>Assignments</h3>
    Never miss deadlines.
    </div>
    """,unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
    <div class="icon">🧮</div>
    <h3>Calculator</h3>
    Quick calculations.
    </div>
    """,unsafe_allow_html=True)

st.write("")
st.markdown("## 🚀 Quick Access")

c1,c2,c3=st.columns(3)

with c1:
    st.button("📖 Open Notes",use_container_width=True)

with c2:
    st.button("📅 Attendance",use_container_width=True)

with c3:
    st.button("🧮 Calculator",use_container_width=True)