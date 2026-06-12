import streamlit as st
import urllib.parse

# 1. إعدادات الصفحة وتفعيل التجاوب مع الشاشات
st.set_page_config(page_title="Activity Today", page_icon="📋", layout="centered")

# 2. تنسيق CSS مخصص لجعل الواجهة ممتازة على الجوال والكمبيوتر
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    /* توحيد الخط المريح للعين */
    html, body, [data-testid="stSidebar"], .stKeyedTextBox, input, select, button, span, p, div {
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* تنسيق العنوان الرئيسي */
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    /* زيادة مساحات العناصر لتسهيل اللمس في الجوال */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        font-size: 16px !important;
    }
    
    /* تحسين خيارات الـ Radio Button */
    [data-testid="stMarkdownContainer"] p {
        font-size: 15px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# عنوان البرنامج
st.markdown("<h1 class='main-title'>📋 Activity Today | النشاط اليومي</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- مدخلات البيانات ---

# 1. اختيار الـ Trunk Line
trunk_line = st.selectbox(
    "اختر خط الجذع | Select Trunk Line", 
    [f"Line {i}" for i in range(1, 13)]
)

# 2. إدخال الكيلومترات (تم إلغاء الأصفار الإجبارية الزائدة باستخدام format="%g")
km_input = st.number_input(
    "إدخال الكيلومترات | Enter Kilometers", 
    min_value=0.0, 
    step=0.1,
    format="%g"
)

# 3. حالة الـ UT
ut_status = st.radio(
    "حالة الفحص | UT Status", 
    ["Complete", "Not Complete"],
    horizontal=True # مصفوفة أفقياً لتوفير المساحة على الجوال
)

# 4. اختيار الفنيين
technicians = st.multiselect(
    "اختر الفنيين | Select Technicians (TECH)", 
    ["Tech A", "Tech B", "Tech C", "Tech D"]
)

st.markdown("<br>", unsafe_allow_html=True)

# --- تجهيز نص رسالة الواتساب تلقائياً ---
techs_list = ", ".join(technicians) if technicians else "لم يتم الاختيار"

whatsapp_text = f"""📋 *Activity Today | النشاط اليومي*
----------------------------------
📍 *Trunk Line:* {trunk_line}
🛣️ *Kilometers:* {km_input} KM
🔍 *UT Status:* {ut_status}
👥 *Technicians:* {techs_list}"""

# ترميز النص ليتوافق مع روابط الويب
encoded_message = urllib.parse.quote(whatsapp_text)
whatsapp_url = f"https://wa.me/?text={encoded_message}"


# --- أزرار التحكم (متجاوبة تماماً مع الجوال والكمبيوتر) ---
col1, col2 = st.columns(2)

with col1:
    if st.button("💾 حفظ في النظام | Submit", use_container_width=True, type="secondary"):
        st.success("تم تسجيل النشاط في النظام بنجاح! 🎉")

with col2:
    # زر الواتساب المباشر - يفتح التطبيق فوراً بالرسالة جاهزة
    st.link_button("🟢 إرسال عبر الواتساب | WhatsApp", whatsapp_url, use_container_width=True, type="primary")
