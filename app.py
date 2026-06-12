import streamlit as st
import urllib.parse

# 1. إعداد الصفحة وتفعيل التجاوب مع الشاشات
st.set_page_config(page_title="Activity Today", page_icon="📋", layout="centered")

# 2. التنسيق الخاص بالخطوط والمظهر (مناسب للجوال والكمبيوتر)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;700&display=swap');
    
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
st.markdown("<h1 class='main-title'>📋 النشاط اليومي المتعدد | Daily Activities</h1>", unsafe_allow_html=True)
st.markdown("---")

# 3. تهيئة الذاكرة التخزينية لحفظ الأنشطة المتعددة
if "activities_list" not in st.session_state:
    st.session_state.activities_list = []

# --- قسم إدخال بيانات النشاط الحالي ---
st.markdown("### 📥 إدخال بيانات النشاط | Enter Activity Details")

# اختيار الخط
trunk_line = st.selectbox(
    "📍 اختر الخط | Select Line", 
    [f"Line {i}" for i in range(1, 13)]
)

# إدخال الكيلومترات
km_input = st.number_input(
    "🛣️ إدخال الكيلومترات | Enter Kilometers", 
    value=0.0,
    min_value=0.0, 
    step=0.001,  # تم تعديل الخطوة لتناسب الفواصل الثلاثية مثل 14.595
    format="%g"
)

# حقل الملاحظات (مثل: extension spool)
remarks_input = st.text_input("📌 ملاحظات إضافية (اختياري) | Remarks")

# حالة الـ UT
ut_status = st.radio(
    "🔍 حالة الفحص | UT Status", 
    ["completed", "Not completed"],
    horizontal=True
)

# قائمة الفنيين المحدثة (إضافة FLC)
technicians = st.multiselect(
    "👥 اختر الفنيين | Select Technicians (TECH)", 
    ["SKT", "SAN", "NAA", "NBO", "HSQ", "HAK", "IAS", "FLC"]
)

st.markdown("<br>", unsafe_allow_width=True)

# --- أزرار التحكم بالأنشطة ---
col1, col2 = st.columns(2)

with col1:
    # زر إضافة النشاط الحالي إلى القائمة
    if st.button("➕ إضافة هذا النشاط | Add Activity", use_container_width=True, type="secondary"):
        line_number = trunk_line.replace("Line ", "")
        km_display = str(km_input) if km_input != 0.0 else "0"
        
        # صياغة سطر الفحص والملاحظات بناءً على نموذجك
        if remarks_input:
            ut_line = f"{remarks_input} UT {ut_status}"
        else:
            ut_line = f"UT {ut_status}"
            
        techs_list = "/".join(technicians) if technicians else "N/A"
        
        # تركيب نص النشاط الواحد
        single_activity = f"TL {line_number} km {km_display}\n{ut_line}\nTech : {techs_list}"
        
        # حفظه في الذاكرة
        st.session_state.activities_list.append(single_activity)
        st.success("✅ تم إدراج النشاط في القائمة بنجاح!")

with col2:
    # زر لمسح كل الأنشطة وبدء قائمة جديدة
    if st.button("🗑️ مسح القائمة | Clear All", use_container_width=True):
        st.session_state.activities_list = []
        st.toast("تم تفريغ القائمة")
        st.rerun()

st.markdown("---")

# --- قسم العرض والإرسال للواتساب ---
if st.session_state.activities_list:
    st.markdown(f"### 👁️ معاينة الرسالة ({len(st.session_state.activities_list)} أنشطة مضافة)")
    
    # تجميع كل الأنشطة مع ترك سطر فارغ بين كل نشاط ونشاط
    all_activities_joined = "\n\n".join(st.session_state.activities_list)
    
    # النص النهائي الكامل لرسالة الواتساب
    final_whatsapp_text = f"📋 Hello Activities today \n\n{all_activities_joined}"
    
    # عرض المعاينة داخل صندوق نصي نظيف
    st.code(final_whatsapp_text, language="text")
    
    # ترميز النص للرابط
    encoded_message = urllib.parse.quote(final_whatsapp_text)
    whatsapp_url = f"https://wa.me/?text={encoded_message}"
    
    # زر الإرسال النهائي الممتد
    st.link_button("🟢 إرسال الكل عبر الواتساب | Send All via WhatsApp", whatsapp_url, use_container_width=True, type="primary")
else:
    st.info("💡 القائمة فارغة حالياً. قم بتعبئة البيانات في الأعلى ثم اضغط على **(إضافة هذا النشاط)** لتتمكن من إنشاء الرسالة وتجميعها.")
