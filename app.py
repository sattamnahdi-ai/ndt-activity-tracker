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

# 3. تهيئة الذاكرة التخزينية وحالات الإشعارات
if "activities_list" not in st.session_state:
    st.session_state.activities_list = []
if "toast_message" not in st.session_state:
    st.session_state.toast_message = None

# --- 4. دالة إضافة النشاط وتفريغ الحقول (Callback) ---
def add_activity_callback():
    line_type = st.session_state.line_type_key
    
    # استخراج القيمة بناءً على نوع الخط (رقم الخط للـ TL، أو اسم المنطقة للـ OSI)
    if line_type == "TL":
        line_val = st.session_state.line_key.replace("Line ", "")
    else:
        line_val = st.session_state.line_key  # ستكون المنطقة مباشرة (KHRS, ABJF, MZLG)
    
    km_display = str(st.session_state.km_key) if st.session_state.km_key != 0.0 else "0"
    
    # صياغة نص الـ UT بحيث تأتي الملاحظات بَعدَه مباشرة
    if st.session_state.remarks_key:
        ut_line = f"UT {st.session_state.ut_key} {st.session_state.remarks_key}"
    else:
        ut_line = f"UT {st.session_state.ut_key}"
        
    techs_list = "/".join(st.session_state.tech_key) if st.session_state.tech_key else "N/A"
    
    # تركيب نص النشاط بالاعتماد على النوع المختار
    single_activity = f"{line_type} {line_val} km {km_display}\n {ut_line}\nTech : {techs_list}"
    
    # حفظ النشاط في القائمة
    st.session_state.activities_list.append(single_activity)
    
    # تفريغ كافة الحقول وإعادتها لوضعها الافتراضي لتهيئتها للنشاط القادم
    st.session_state.line_type_key = "TL"
    st.session_state.line_key = "Line 1"
    st.session_state.km_key = 0.0
    st.session_state.remarks_key = ""
    st.session_state.ut_key = "completed"
    st.session_state.tech_key = []
    
    # تجهيز إشعار النجاح
    st.session_state.toast_message = "✅ تم حفظ النشاط وتفريغ الحقول!"

# دالة مسح القائمة بالكامل (Callback)
def clear_all_callback():
    st.session_state.activities_list = []
    st.session_state.toast_message = "🗑️ تم مسح جميع الأنشطة"

# --- عرض الإشعارات إن وجدت ---
if st.session_state.toast_message:
    st.toast(st.session_state.toast_message)
    st.session_state.toast_message = None


# --- قسم إدخال بيانات النشاط الحالي ---
st.markdown("### 📥 إدخال بيانات النشاط | Enter Activity Details")

# اختيار نوع الخط (TL أو OSI)
st.radio(
    "🏷️ نوع الخط | Line Type",
    ["TL", "OSI"],
    horizontal=True,
    key="line_type_key"
)

# 🔄 التعديل الجديد: تغيير المسمى والخيارات ديناميكياً مع حماية الـ الذاكرة من التعارض
if st.session_state.line_type_key == "TL":
    # إذا تحول المستخدم لـ TL وكانت القيمة السابقة منطقة، نعيد تصفيرها لخيار الخطوط لمنع حدوث خطأ
    if "line_key" in st.session_state and st.session_state.line_key not in [f"Line {i}" for i in range(1, 13)]:
        st.session_state.line_key = "Line 1"
        
    st.selectbox(
        "📍 اختر رقم الخط | Select Line Number", 
        [f"Line {i}" for i in range(1, 13)],
        key="line_key"
    )
else:
    # إذا تحول المستخدم لـ OSI وكان مخزن خط قديم، نغيره فوراً إلى أول منطقة لمنع حدوث خطأ
    if "line_key" in st.session_state and st.session_state.line_key not in ["KHRS", "ABJF", "MZLG"]:
        st.session_state.line_key = "KHRS"
        
    st.selectbox(
        "📍 اختر المنطقة | Select Area", 
        ["KHRS", "ABJF", "MZLG"],
        key="line_key"
    )

# إدخال الكيلومترات
st.number_input(
    "🛣️ إدخال الكيلومترات | Enter Kilometers", 
    value=0.0,
    min_value=0.0, 
    step=0.001,
    format="%g",
    key="km_key"
)

# حالة الـ UT
st.radio(
    "🔍 حالة الفحص | UT Status", 
    ["completed", "Not completed"],
    horizontal=True,
    key="ut_key"
)

# حقل الملاحظات
st.text_input("📌 ملاحظات إضافية (اختياري) | Remarks", key="remarks_key")

# قائمة الفنيين
st.multiselect(
    "👥 اختر الفنيين | Select Technicians (TECH)", 
    ["SKT", "SAN", "NAA", "NBO", "HSQ", "HAK", "IAS", "FLC"],
    key="tech_key"
)

st.markdown("<br>", unsafe_allow_html=True)

# --- أزرار التحكم بالأنشطة باستخدام الـ Callbacks ---
col1, col2 = st.columns(2)

with col1:
    st.button(
        "➕ إضافة هذا النشاط | Add Activity", 
        use_container_width=True, 
        type="secondary",
        on_click=add_activity_callback
    )

with col2:
    st.button(
        "🗑️ مسح القائمة | Clear All", 
        use_container_width=True,
        on_click=clear_all_callback
    )

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
