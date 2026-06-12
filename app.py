import streamlit as st
import urllib.parse

# 1. إعداد الصفحة
st.set_page_config(page_title="Activity Today", page_icon="📋", layout="centered")

# 2. التنسيق الخاص بالخطوط والمظهر (مناسب للجوال والكمبيوتر)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .stKeyedTextBox, input, select, button, span, p, div {
        font-family: 'Cairo', sans-serif !important;
    }
    
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    div[data-baseweb="select"], div[data-baseweb="input"] {
        font-size: 16px !important;
    }
    
    [data-testid="stMarkdownContainer"] p {
        font-size: 15px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# عنوان البرنامج الرئيسي
st.markdown("<h1 class='main-title'>النشاط اليومي | Activity Today</h1>", unsafe_allow_html=True)
st.markdown("---")

# 1. اختيار الخط
trunk_line = st.selectbox(
    "اختر الخط | Select Line", 
    [f"Line {i}" for i in range(1, 13)]
)

# 2. إدخال الكيلومترات (يبدأ فارغ وبدون أصفار تلقائية)
km_input = st.number_input(
    "إدخال الكيلومترات | Enter Kilometers", 
    value=None,
    min_value=0.0, 
    step=0.1,
    format="%g"
)

# 3. حالة الـ UT
ut_status = st.radio(
    "حالة الفحص | UT Status", 
    ["Complete", "Not Complete"],
    horizontal=True
)

# 4. اختيار الفنيين
technicians = st.multiselect(
    "اختر الفنيين | Select Technicians (TECH)", 
    ["Tech A", "Tech B", "Tech C", "Tech D"]
)

st.markdown("<br>", unsafe_allow_html=True)

# 5. تجهيز نص الواتساب الرسمي والعملي (بدون إيموجيات)
techs_list = ", ".join(technicians) if technicians else "N/A"
km_display = km_input if km_input is not None else ""

whatsapp_text = f"""Activity Today Report
---------------------
Trunk Line: {trunk_line}
Kilometers: {km_display} KM
UT Status: {ut_status}
Technicians: {techs_list}"""

# ترميز النص للرابط ليتوافق مع المتصفحات والتطبيق
encoded_message = urllib.parse.quote(whatsapp_text)
whatsapp_url = f"https://wa.me/?text={encoded_message}"

# زر إرسال عبر الواتساب ممتد بالكامل ليناسب شاشات الجوال
st.link_button("إرسال عبر الواتساب | WhatsApp", whatsapp_url, use_container_width=True, type="primary")
