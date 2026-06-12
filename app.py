import streamlit as st

st.set_page_config(page_title="Activity Today", page_icon="📋")

st.markdown("<h1 style='text-align: center;'>📋 Activity Today</h1>", unsafe_allow_html=True)

# 1. Trunk Line selection
trunk_line = st.selectbox("Select Trunk Line", [f"Line {i}" for i in range(1, 13)])

# 2. Kilometer input
km_input = st.number_input("Enter Kilometers", min_value=0.0, step=0.1)

# 3. UT Status
ut_status = st.radio("UT Status", ["Complete", "Not Complete"])

# 4. Technician selection
technicians = st.multiselect("Select Technicians (TECH)", ["Tech A", "Tech B", "Tech C", "Tech D"])

if st.button("Submit"):
    st.success("Activity logged successfully! 🎉")
