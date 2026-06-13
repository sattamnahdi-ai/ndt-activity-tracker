import streamlit as st
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Activity Today", page_icon="📋", layout="centered")

# 2. Initialize Session States (Updated Defaults for Mobile/User preference)
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
        "line_num": "📍 Select Line Number",
        "area": "📍 Select Area",
        "km": "🛣️ Enter Kilometers",
        "wh": "🛢️ Enter Well Number / Well Head",
        "wh_placeholder": "e.g., 12 or KHRS-45",
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
        "line_num": "📍 اختر رقم الخط",
        "area": "📍 اختر المنطقة",
        "km": "🛣️ إدخال الكيلومترات",
        "wh": "🛢️ رقم العين أو الـ Well Head",
        "wh_placeholder": "مثال: 12 أو KHRS-45",
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
    
    /* Base Text / Labels Handling - Responsive sizes */
    label p, .stRadio label, div[role="radiogroup"] label, [data-testid="stWidgetLabel"] p {{
        color: {text_color} !important;
        font-family: 'Cairo', sans-serif !important;
        text-align: {text_align};
        font-size: 14px !important;
    }}
    
    /* Responsive Title for Mobile Screen */
    .main-title {{
        color: #1E88E5 !important;
        text-align: center !important;
        font-size: calc(18px + 1vw) !important;
        font-weight: 700;
        margin-bottom: 15px;
        padding: 0 5px;
    }}
    
    /* Inputs, Select boxes Optimized for Mobile */
    div[data-baseweb="input"], div[data-baseweb="select"], .stSelectbox div, .stTextInput input, .stNumberInput input {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {btn_border} !important;
        border-radius: 8px !important;
        min-height: 42px !important;
    }}
    input {{
        color: {text_color} !important;
    }}
    
    /* Multi-Select Tags */
    div[data-baseweb="tag"] {{
        background-color: {tag_bg} !important;
        border-radius: 6px !important;
        padding: 4px 10px !important;
        margin: 3px !important;
    }}
    div[data-baseweb="tag"] * {{
        color: {tag_text} !important;
        fill: {tag_text} !important;
    }}
    
    /* Dropdown Menu Popover Alignment */
    div[data-baseweb="popover"], div[role="listbox"] {{
        background-color: {card_bg} !important;
    }}
    div[data-baseweb="popover"] li, div[role="option"] {{
        color: {text_color} !important;
        background-color: {card_bg} !important;
    }}
    
    /* Buttons Optimized as Mobile Touch Targets (Min Height 44px) */
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {btn_text} !important;
        border: 1px solid {btn_border} !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        min-height: 45px !important;
        font-size: 15px !important;
    }}
    div.stButton > button:hover {{
        border-color: #1E88E5 !important;
        color: #1E88E5 !important;
        background-color: {input_bg} !important;
    }}
    
    /* WhatsApp Button Mobile Style */
    div.stButton > button[kind="primary"] {{
        background-color: #1E88E5 !important;
        color: #FFFFFF !important;
        border: none !important;
        min-height: 48px !important;
    }}

    /* Controls Row - Strict side-by-side on mobile screen without wrapping */
    div[data-testid="stHorizontalBlock"]:has(.top-ctrl-lang) {{
        direction: ltr !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: flex-start !important;
        gap: 10px !important;
        margin-bottom: 5px;
    }}
    div[data-testid="stHorizontalBlock"]:has(.top-ctrl-lang) div[data-testid="column"] {{
        width: max-content !important;
        flex: none !important;
    }}
    
    /* Fixed Top Control Buttons Style */
    div[data-testid="column"]:has(.top-ctrl-lang) button,
    div[data-testid="column"]:has(.top-ctrl-theme) button {{
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        max-width: 44px !important;
        padding: 0 !important;
        font-size: 18px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 8px !important;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 5. Top Controls (Language & Theme Switchers - strictly row layout)
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

# App Main Title
st.markdown(f"<h1 class='main-title'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- 6. Callback Functions ---
def add_activity_callback():
    act_type = st.session_state.line_type_key
    
    # 1. Build the UT Line
    if st.session_state.remarks_key:
        ut_line = f"UT {st.session_state.ut_key} {st.session_state.remarks_key}"
    else:
        ut_line = f"UT {st.session_state.ut_key}"
        
    # 2. Build the Technicians List
    techs_list = "/".join(st.session_state.tech_key) if st.session_state.tech_key else "N/A"
    
    # 3. Dynamic formatting based on type (TL vs OSI)
    if act_type == "TL":
        line_val = st.session_state.line_key.replace("Line ", "")
        km_display = str(st.session_state.km_key) if st.session_state.km_key != 0.0 else "0"
        location_part = f"km {km_display}"
        single_activity = f"{act_type} {line_val} {location_part}\n {ut_line}\nTech : {techs_list}"
    else:
        area_val = st.session_state.line_key
        wh_display = st.session_state.wh_key if ("wh_key" in st.session_state and st.session_state.wh_key) else "0"
        single_activity = f"{area_val}-{wh_display} OSI\n {ut_line}\nTech : {techs_list}"
    
    # Save to list
    st.session_state.activities_list.append(single_activity)
    
    # Reset Fields
    st.session_state.line_type_key = "TL"
    st.session_state.line_key = "Line 1"
    st.session_state.km_key = 0.0
    st.session_state.wh_key = ""
    st.session_state.remarks_key = ""
    st.session_state.ut_key = "completed"
    st.session_state.tech_key = []
    
    st.session_state.toast_message = t["success_toast"]

def clear_all_callback():
    st.session_state.activities_list = []
    st.session_state.toast_message = t["clear_toast"]

# Display Toasts
if st.session_state.toast_message:
    st.toast(st.session_state.toast_message)
    st.session_state.toast_message = None


# --- 7. Activity Input Section ---
st.markdown(f"### {t['input_header']}")

# Type of Activity
st.radio(
    t["act_type"],
    ["TL", "OSI"],
    horizontal=True,
    key="line_type_key"
)

# Dynamic UI adjustments based on Activity Type
if st.session_state.line_type_key == "TL":
    if "line_key" in st.session_state and st.session_state.line_key not in [f"Line {i}" for i in range(1, 13)]:
        st.session_state.line_key = "Line 1"
        
    st.selectbox(
        t["line_num"], 
        [f"Line {i}" for i in range(1, 13)],
        key="line_key"
    )
    
    st.number_input(
        t["km"], 
        value=0.0,
        min_value=0.0, 
        step=0.001,
        format="%g",
        key="km_key"
    )
else:
    if "line_key" in st.session_state and st.session_state.line_key not in ["KHRS", "ABJF", "MZLG"]:
        st.session_state.line_key = "KHRS"
        
    st.selectbox(
        t["area"], 
        ["KHRS", "ABJF", "MZLG"],
        key="line_key"
    )
    
    st.text_input(
        t["wh"],
        key="wh_key",
        placeholder=t["wh_placeholder"]
    )

# UT Status
st.radio(
    t["ut"], 
    ["completed", "Not completed"],
    horizontal=True,
    key="ut_key"
)

# Remarks
st.text_input(t["remarks"], key="remarks_key")

# Technicians
st.multiselect(
    t["techs"], 
    ["SKT", "SAN", "NAA", "NBO", "HSQ", "HAK", "IAS", "FLC"],
    key="tech_key"
)

st.markdown("<br>", unsafe_allow_html=True)

# --- 8. Action Buttons ---
col1, col2 = st.columns(2)

with col1:
    st.button(
        t["add_btn"], 
        use_container_width=True, 
        type="secondary",
        on_click=add_activity_callback
    )

with col2:
    st.button(
        t["clear_btn"], 
        use_container_width=True,
        on_click=clear_all_callback
    )

st.markdown("---")

# --- 9. Preview and Send Section ---
if st.session_state.activities_list:
    st.markdown(f"### {t['preview'].format(count=len(st.session_state.activities_list))}")
    
    all_activities_joined = "\n\n".join(st.session_state.activities_list)
    final_whatsapp_text = f"📋 Hello Activities today \n\n{all_activities_joined}"
    
    st.code(final_whatsapp_text, language="text")
    
    encoded_message = urllib.parse.quote(final_whatsapp_text)
    whatsapp_url = f"https://wa.me/?text={encoded_message}"
    
    st.link_button(t["send_wa"], whatsapp_url, use_container_width=True, type="primary")
else:
    st.info(t["empty"])

