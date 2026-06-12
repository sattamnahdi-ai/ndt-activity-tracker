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

# اختيار الخط (مع إضافة key للتحكم بالمسح)
trunk_line = st.selectbox(
    "📍 اختر الخط | Select Line", 
    [f"Line {i}" for i in range(1, 13)],
    key="line_key"
)

# إدخال الكيلومترات (مع إضافة key للتحكم بالمسح)
km_input = st.number_input(
    "🛣️ إدخال الكيلومترات | Enter Kilometers", 
    value=0.0,
    min_value=0.0, 
    step=0.001,
    format="%g",
    key="km_key"
)

# حالة الـ UT (مع إضافة key للتحكم بالمسح)
ut_status = st.radio(
    "🔍 حالة الفحص | UT Status", 
    ["completed", "Not completed"],
    horizontal=True,
    key="ut_key"
)

# حقل الملاحظات - أصبح اختياري ويظهر بعد الـ UT (مع إضافة key للتحكم بالمسح)
remarks_input = st.text_input("📌 ملاحظات إضافية (اختياري) | Remarks", key="remarks_key")

# قائمة الفنيين (مع إضافة key للتحكم بالمسح)
technicians = st.multiselect(
    "👥 اختر الفنيين | Select Technicians (TECH)", 
    ["SKT", "SAN", "NAA", "NBO", "HSQ", "HAK", "IAS", "FLC"],
    key="tech_key"
)

st.markdown("<br>", unsafe_allow_html=True)

# --- أزرار التحكم بالأنشطة ---
col1, col2 = st.columns(2)

with col1:
    # زر إضافة النشاط الحالي إلى القائمة وتفريغ الحقول
    if st.button("➕ إضافة هذا النشاط | Add Activity", use_container_width=True, type="secondary"):
        line_number = st.session_state.line_key.replace("Line ", "")
        km_display = str(st.session_state.km_key) if st.session_state.km_key != 0.0 else "0"
        
        # التعديل الجديد: صياغة نص الـ UT بحيث تأتي الملاحظات بَعدَه مباشرة
        if st.session_state.remarks_key:
            ut_line = f"UT {st.session_state.ut_key} {st.session_state.remarks_key}"
        else:
            ut_line = f"UT {st.session_state.ut_key}"
            
        techs_list = "/".join(st.session_state.tech_key) if st.session_state.tech_key else "N/A"
        
        # تركيب نص النشاط
        single_activity = f"TL {line_number} km {km_display}\n {ut_line}\nTech : {techs_list}"
        
        # حفظ النشاط في القائمة
        st.session_state.activities_list.append(single_activity)
        
        # الحــل: تفريغ كافة الحقول وإعادتها لوضعها الافتراضي فوراً للنشاط القادم
        st.session_state.line_key = "Line 1"
        st.session_state.km_key = 0.0
        st.session_state.remarks_key = ""
        st.session_state.ut_key = "completed"
        st.session_state.tech_key = []
        
        # إشعار سريع بنجاح العملية وإعادة تحديث الصفحة
        st.toast("✅ تم حفظ النشاط وتفريغ الحقول!")
        st.rerun()

with col2:
    # زر لمسح كل الأنشطة وبدء قائمة جديدة تماماً
    if st.button("🗑️ مسح القائمة | Clear All", use_container_width=True):
        st.session_state.activities_list = []
        st.toast("تم مسح جميع الأنشطة")
        st.rerun()

st.markdown("---")

# --- قسم العرض والإرسال للواتساب ---
if st.session_state.activities_list:
    st.markdown(f"### 👁️ معاينة الرسالة ({len(st.session_state.activities_list)} أنشطة مضافة)")
    
    # تجميع كل الأنشطة مع ترك سطر فارغ بين كل نشاط ونشاط
    all_activities_joined = "\n\n".join(st.session_state.activities_list)
    
    # النص النهائي الكامل لرسالة الواتساب
    final_whatsapp_text = f"📋 Hello Activities today \n\n{all_activities_joined}"
    
    # عرض المعاينة داخل صندوق نصي
    st.code(final_whatsapp_text, language="text")
    
    # ترميز النص للرابط
    encoded_message = urllib.parse.quote(final_whatsapp_text)
    whatsapp_url = f"https://wa.me/?text={encoded_message}"
    
    # زر الإرسال النهائي
    st.link_button("🟢 إرسال الكل عبر الواتساب | Send All via WhatsApp", whatsapp_url, use_container_width=True, type="primary")
else:
    st.info("💡 القائمة فارغة حالياً. قم بتعبئة البيانات في الأعلى ثم اضغط على **(إضافة هذا النشاط)** لتتمكن من إنشاء الرسالة وتجميعها.")
