import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="Activity Today", page_icon="📋", layout="centered")

# 2. إضافة التعديلات الخاصة بالخطوط والتنسيق (CSS) ليكون المظهر احترافي
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    /* تغيير الخط للبرنامج بالكامل */
    html, body, [data-testid="stSidebar"], .stKeyedTextBox, input, select, button, span {
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* تنسيق العنوان الرئيسي */
    .main-title {
        text-align: center;
        color: #007bff;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 25px;
    }
    
    /* تنسيق زر الإرسال */
    .stButton>button {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100%;
        border-radius: 8px;
        padding: 10px;
        border: none;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# العنوان الرئيسي للملف بعد التعديل
st.markdown("<h1 class='main-title'>📋 Activity Today | النشاط اليومي</h1>", unsafe_allow_html=True)
st.markdown("---")

# 1. اختيار الـ Trunk Line
trunk_line = st.selectbox(
    "اختر خط الجذع | Select Trunk Line", 
    [f"Line {i}" for i in range(1, 13)]
)

# 2. إدخال الكيلومترات
km_input = st.number_input(
    "إدخال الكيلومترات | Enter Kilometers", 
    min_value=0.0, 
    step=0.1
)

# 3. حالة الـ UT (كامل أو غير كامل)
ut_status = st.radio(
    "حالة الفحص | UT Status", 
    ["Complete", "Not Complete"]
)

# 4. اختيار الفنيين (Technicians)
technicians = st.multiselect(
    "اختر الفنيين | Select Technicians (TECH)", 
    ["Tech A", "Tech B", "Tech C", "Tech D"]
)

st.markdown("<br>", unsafe_allow_html=True)

# زر الإرسال مع التعديل الجديد
if st.button("إرسال النشاط | Submit Activity"):
    st.success("تم تسجيل النشاط بنجاح! 🎉 | Activity logged successfully!")
