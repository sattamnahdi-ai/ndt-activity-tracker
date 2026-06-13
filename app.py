import streamlit as st
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Activity Today", page_icon="📋", layout="centered")

# 2. Initialize Session States
if "activities_list" not in st.session_state:
    st.session_state.activities_list = []
if "toast_message" not in st.session_state:
    st.session_state.toast_message = None
if "lang" not in st.session_state:
    st.session_state.lang = "EN"  # Default language is English
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"  # Default theme set to Dark Mode

# 3. Translation Dictionary
translations = {
    "EN": {
        "title": "📋 Daily Activities Tracker",
        "input_header": "📥 Enter Activity Details",
        "act_type": "🏷️ Type of Activity",
        "custom_act": "✍️ Enter Custom Activity Type",
        "line_num": "📍 Select Line Number",
        "area": "📍 Select Area",
        "km": "🛣️ Enter Kilometers",
        "wh": "🛢️ Enter Well Number / Well Head (Numbers Only)",
        "ut": "🔍 UT Status",
        "remarks": "📌 Remarks (Optional)",
        "techs": "👥 Select Technicians (TECH)",
        "add_btn": "➕ Add Activity",
        "clear_btn": "🗑️ Clear All",
        "preview": "👁️ Message Preview ({count} activities added)",
        "send_wa": "🟢 Send All via WhatsApp",
        "empty": "💡 The list is currently empty. Fill in the details above and click (Add Activity) to compile the message.",
        "success_toast": "✅ Activity saved and fields cleared!",
        "clear_toast": "🗑️ All activities cleared",
        "toggle_lang": "🌐 Switch to العربية",
        "toggle_theme": "🌙 Dark Mode" if st.session_state.theme == "Light" else "☀️ Light Mode"
    },
    "AR": {
        "title": "📋 متتبع الأنشطة اليومية",
        "input_header": "📥 إدخل بيانات النشاط",
        "act_type": "🏷️ نوع النشاط",
        "custom_act": "✍️ أدخل نوع النشاط المخصص",
        "line_num": "📍 اختر رقم الخط",
        "area": "📍 اختر المنطقة",
        "km": "🛣️ إدخال الكيلومترات",
        "wh": "🛢️ رقم العين أو الـ Well Head (أرقام فقط)",
        "ut": "🔍 حالة الفحص",
        "remarks": "📌 ملاحظات إضافية (اختياري)",
        "techs": "👥 اختر الفنيين (TECH)",
        "add_btn": "➕ إضافة هذا النشاط",
        "clear_btn": "🗑️ مسح القائمة",
        "preview": "👁️ معاينة الرسالة ({count} أنشطة مضافة)",
        "send_wa": "🟢 إرسال الكل عبر الواتساب",
        "empty": "💡 القائمة فارغة حالياً. قم بتعبئة البيانات في الأعلى ثم اضغط على (إضافة هذا النشاط) لتتمكن من إنشاء الرسالة وتجميعها.",
        "success_toast": "✅ تم حفظ النشاط وتفريغ الحقول!",
        "clear_toast": "🗑️ تم مسح جميع الأنشطة",
        "toggle_lang": "🌐 Switch to English",
        "toggle_theme": "🌙 الوضع الليلي" if st.session_state.theme == "Light" else "☀️ الوضع النهاري"
    }
}

t = translations[st.session_state.lang]

# 4. Advanced Theme & Dynamic Color Configurations
direction = "rtl" if st.session_state.lang == "AR" else "ltr"
text_align = "right" if st.session_state.lang == "AR" else "left"

if st.session_state.theme == "Dark":
    bg_color = "#0E1117"
    text_color = "#FAFAFA"
    input_bg = "#262730"
    btn_bg = "#262730"
    btn_text = "#FAFAFA"
    btn_border = "#4A4B50"
    tag_bg = "#1E293B"     
    tag_text = "#93C5FD"   
    card_bg = "#1E293B"
else:
    bg_color = "#F8F9FA"  
    text_color = "#212529"  
    input_bg = "#FFFFFF"  
    btn_bg = "#FFFFFF"
    btn_text = "#212529"
    btn_border = "#CED4DA"  
    tag_bg = "#E3F2FD"     
    tag_text = "#0D47A1"   
    card_bg = "#FFFFFF"

custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;700&display=swap');
    
    /* Base App Container & Mobile Optimization */
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {bg_color} !important;
        font-family: 'Cairo', sans-serif !important;
        direction: {direction};
        padding: 10px !important;
    }}
    
    /* Base Text / Labels Handling */
    label p, .stRadio label, div[role="radiogroup"] label, [data-testid="stWidgetLabel"] p {{
        color: {text_color} !important;
        font-family: 'Cairo', sans-serif !important;
        text-align: {text_align};
        font-size: 14px !important;
    }}
    
    .main-title {{
        color: #1E88E5 !important;
        text-align: center !important;
        font-size: calc(18px + 1vw) !important;
        font-weight: 700;
        margin-bottom: 15px;
    }}
    
    /* Inputs, Select boxes Optimized for Mobile */
    div[data-baseweb="input"], div[data-baseweb="select"], .stSelectbox div, .stTextInput input, .stNumberInput input {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {btn_border} !important;
        border-radius: 8px !important;
        min-height: 42px !important;
    }}
    
    /* Multi-Select Tags */
    div[data-baseweb="tag"] {{
        background-color: {tag_bg} !important;
        border-radius: 6px !important;
        padding: 4px 10px !important;
    }}
    div[data-baseweb="tag"] * {{
        color: {tag_text} !important;
        fill: {tag_text} !important;
    }}
    
    /* Buttons Optimized as Mobile Touch Targets */
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {btn_text} !important;
        border: 1px solid {btn_border} !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        width: 100% !important;
        min-height: 45px !important;
    }}
    
    /* WhatsApp Button Style */
    div.stButton > button[kind="primary"] {{
        background-color: #1E88E5 !important;
        color: #FFFFFF !important;
        border: none !important;
    }}

    /* Controls Row side-by-side */
    div[data-testid="stHorizontalBlock"]:has(.top-ctrl-lang) {{
        direction: ltr !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.top-ctrl-lang) div[data-testid="column"] {{
        width: max-content !important;
        flex: none !important;
    }}
    
    div[data-testid="column"]:has(.top-ctrl-lang) button,
    div[data-testid="column"]:has(.top-ctrl-theme) button {{
        width: 44px !important;
        height: 44px !important;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 5. Top Controls (Language & Theme Switchers)
col_lang, col_theme, _ = st.columns([1, 1, 12])

with col_lang:
    st.markdown('<span class="top-ctrl-lang"></span>', unsafe_allow_html=True)
    if st.button("🌐", key="lang_btn", help=t["toggle_lang"]):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()

with col_theme:
    st.markdown('<span class="top-ctrl-theme"></span>', unsafe_allow_html=True)
    theme_emoji = "☀️" if st.session_state.theme == "Dark" else "🌙"
    if st.button(theme_emoji, key="theme_btn", help=t["toggle_theme"]):
        st.session_state.theme = "Dark" if st.session_state.theme == "Light" else "Light"
        st.rerun()

st.markdown(f"<h1 class='main-title'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- 6. Callback Functions ---
def add_activity_callback():
    act_type = st.session_state.line_type_key
    
    # Build UT Line
    if st.session_state.remarks_key:
        ut_line = f"UT {st.session_state.ut_key} {st.session_state.remarks_key}"
    else:
        ut_line = f"UT {st.session_state.ut_key}"
        
    # Build Technicians List
    techs_list = "/".join(st.session_state.tech_key) if st.session_state.tech_key else "N/A"
    
    # Dynamic formatting based on type
    if act_type == "TL":
        line_val = st.session_state.line_key.replace("Line ", "")
        km_display = str(st.session_state.km_key) if st.session_state.km_key != 0.0 else "0"
        single_activity = f"{act_type} {line_val} km {km_display}\n {ut_line}\nTech : {techs_list}"
    elif act_type == "OSI":
        area_val = st.session_state.line_key
        wh_display = str(st.session_state.wh_key) if "wh_key" in st.session_state else "0"
        single_activity = f"{area_val}-{wh_display} OSI\n {ut_line}\nTech : {techs_list}"
    else:  # Other (Free option)
        custom_val = st.session_state.custom_act_key if st.session_state.custom_act_key else "Custom Activity"
        single_activity = f"{custom_val}\n {ut_line}\nTech : {techs_list}"
    
    st.session_state.activities_list.append(single_activity)
    
    # Reset Fields
    st.session_state.line_type_key = "TL"
    st.session_state.line_key = "Line 1"
    st.session_state.km_key = 0.0
    st.session_state.wh_key = 0
    st.session_state.custom_act_key = ""
    st.session_state.remarks_key = ""
    st.session_state.ut_key = "completed"
    st.session_state.tech_key = []
    
    st.session_state.toast_message = t["success_toast"]

def clear_all_callback():
    st.session_state.activities_list = []
    st.session_state.toast_message = t["clear_toast"]

if st.session_state.toast_message:
    st.toast(st.session_state.toast_message)
    st.session_state.toast_message = None

# --- 7. Activity Input Section ---
st.markdown(f"### {t['input_header']}")

# Type of Activity (Added "Other" for free choice)
st.radio(
    t["act_type"],
    ["TL", "OSI", "Other"],
    horizontal=True,
    key="line_type_key"
)

# Render inputs dynamically based on selection
if st.session_state.line_type_key == "TL":
    if "line_key" in st.session_state and st.session_state.line_key not in [f"Line {i}" for i in range(1, 13)]:
        st.session_state.line_key = "Line 1"
    st.selectbox(t["line_num"], [f"Line {i}" for i in range(1, 13)], key="line_key")
    st.number_input(t["km"], value=0.0, min_value=0.0, step=0.001, format="%g", key="km_key")

elif st.session_state.line_type_key == "OSI":
    # Updated MZLG to MZLJ
    if "line_key" in st.session_state and st.session_state.line_key not in ["KHRS", "ABJF", "MZLJ"]:
        st.session_state.line_key = "KHRS"
    st.selectbox(t["area"], ["KHRS", "ABJF", "MZLJ"], key="line_key")
    # Changed Well Head to Numbers Only
    st.number_input(t["wh"], value=0, min_value=0, step=1, key="wh_key")

else:  # Other Free Text Option
    st.text_input(t["custom_act"], key="custom_act_key", placeholder="e.g., PM, Inspection, Rig down...")

# UT Status & Remarks
st.radio(t["ut"], ["completed", "Not completed"], horizontal=True, key="ut_key")
st.text_input(t["remarks"], key="remarks_key")

# Technicians
st.multiselect(t["techs"], ["SKT", "SAN", "NAA", "NBO", "HSQ", "HAK", "IAS", "FLC"], key="tech_key")

st.markdown("<br>", unsafe_allow_html=True)

# --- 8. Action Buttons ---
col1, col2 = st.columns(2)
with col1:
    st.button(t["add_btn"], use_container_width=True, type="secondary", on_click=add_activity_callback)
with col2:
    st.button(t["clear_btn"], use_container_width=True, on_click=clear_all_callback)

st.markdown("---")

# --- 9. Preview and Send Section with Edit Support ---
if st.session_state.activities_list:
    st.markdown(f"### {t['preview'].format(count=len(st.session_state.activities_list))}")
    
    # Inline loop for viewing and editing each activity individually
    for i, activity in enumerate(st.session_state.activities_list):
        if st.session_state.get(f"editing_{i}", False):
            # Edit mode
            st.text_area(f"Modify Activity {i+1}", value=activity, key=f"act_input_{i}")
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("💾 Save", key=f"save_{i}"):
                    st.session_state.activities_list[i] = st.session_state[f"act_input_{i}"]
                    st.session_state[f"editing_{i}"] = False
                    st.rerun()
            with col_cancel:
                if st.button("❌ Cancel", key=f"cancel_{i}"):
                    st.session_state[f"editing_{i}"] = False
                    st.rerun()
        else:
            # View mode with Edit Button
            st.code(activity, language="text")
            if st.button(f"✏️ Edit Activity {i+1}", key=f"edit_btn_{i}"):
                st.session_state[f"editing_{i}"] = True
                st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            
    st.markdown("---")
    
    # Final Full Message Preview
    all_activities_joined = "\n\n".join(st.session_state.activities_list)
    final_whatsapp_text = f"📋 Hello Activities today \n\n{all_activities_joined}"
    
    st.markdown("### 🟢 Final Combined Message")
    st.code(final_whatsapp_text, language="text")
    
    encoded_message = urllib.parse.quote(final_whatsapp_text)
    whatsapp_url = f"https://wa.me/?text={encoded_message}"
    st.link_button(t["send_wa"], whatsapp_url, use_container_width=True, type="primary")
else:
    st.info(t["empty"])
