import streamlit as st
import urllib.parse

# 1. إعداد الصفحة وتفعيل التجاوب مع الشاشات
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
st.markdown("<h1 class='main-title'>📋 النشاط اليومي | Activity Today</h1>", unsafe_allow_html=True)
st.markdown("---")

# 1. اختيار الخط
trunk_line = st.selectbox(
    "📍 اختر الخط | Select Line", 
    [f"Line {i}" for i in range(1, 13)]
)

# 2. إدخال الكيلومترات كحقل رقمي (يفتح الكيبورد الرقمي تلقائياً في الجوال)
km_input = st.number_input(
    "🛣️ إدخال الكيلومترات | Enter Kilometers", 
    value=0.0,
    min_value=0.0, 
    step=0.1,
    format="%g"
)

# 3. حقل الملاحظات (Remarks)
remarks_input = st.text_input("📌 ملاحظات | Remarks")

# 4. حالة الـ UT
ut_status = st.radio(
    "🔍 حالة الفحص | UT Status", 
    ["Complete", "Not Complete"],
    horizontal=True
)

# 5. اختيار الفنيين بالاختصارات الجديدة المطلوبة
technicians = st.multiselect(
    "👥 اختر الفنيين | Select Technicians (TECH)", 
    ["SKT", "SAN", "NAA", "NBO", "HSQ", "HAK", "IAS"]
)

st.markdown("<br>", unsafe_allow_html=True)

# --- تجهيز نص رسالة الواتساب المختصرة والاحترافية ---
line_number = trunk_line.replace("Line ", "")
km_display = str(km_input) if km_input != 0.0 else "0"

# ضبط صيغة حالة الـ UT وإضافة الملاحظة بجانبها بين قوسين لو وُجدت
ut_text = f"UT {ut_status}"
if remarks_input:
    ut_text += f" ({remarks_input})"

techs_list = " / ".join(technicians) if technicians else "N/A"

# نص الرسالة النهائي مع نقل الإيموجي إلى بداية السطر
whatsapp_text = f"""📋 Hello Activities today

📍 TL {line_number} km {km_display}
🔍 {ut_text}
👥 Tech: {techs_list}"""

# ترميز النص للرابط ليتوافق مع التطبيق والمتصفح
encoded_message = urllib.parse.quote(whatsapp_text)
whatsapp_url = f"https://wa.me/?text={encoded_message}"

# زر إرسال عبر الواتساب ممتد بالكامل ليناسب شاشات الجوال والكمبيوتر
st.link_button("🟢 إرسال عبر الواتساب | WhatsApp", whatsapp_url, use_container_width=True, type="primary")
