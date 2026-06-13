import streamlit as st
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Activities Tracker", page_icon=None, layout="centered")

# 2. Initialize Session States
if "activities_list" not in st.session_state:
    st.session_state.activities_list = []
if "toast_message" not in st.session_state:
    st.session_state.toast_message = None
if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# 3. Professional Translation Dictionary (No Emojis)
translations = {
    "EN": {
        "title": "Daily Activities Tracker",
        "input_header": "Activity Details Entry",
        "act_type": "Type of Activity",
        "custom_act": "Enter Custom Activity Type",
        "line_num": "Select Line Number",
        "area": "Select Area",
        "km": "Enter Kilometers",
        "wh": "Enter Well Head Number",
        "ut": "UT Status",
        "remarks": "Remarks (Optional)",
        "techs": "Select Technicians",
        "add_btn": "Add Activity",
        "clear_btn": "Clear All",
        "preview": "Message Preview ({count} activities added)",
        "final_msg": "Final Combined Message",
        "send_wa": "Send via WhatsApp",
        "empty": "The list is currently empty. Fill in the details above and click Add Activity to compile the message.",
        "success_toast": "Activity saved successfully.",
        "clear_toast": "All activities cleared.",
        "toggle_lang": "العربية",
        "toggle_theme": "Light Mode" if st.session_state.theme == "Dark" else "Dark Mode",
        "save": "Save",
        "cancel": "Cancel",
        "edit_btn": "Edit Activity",
        "modify_title": "Modify Activity"
    },
    "AR": {
        "title": "متتبع الأنشطة اليومية",
        "input_header": "إدخل بيانات النشاط",
        "act_type": "نوع النشاط",
        "custom_act": "أدخل نوع النشاط المخصص",
        "line_num": "اختر رقم الخط",
        "area": "اختر المنطقة",
        "km": "إدخال الكيلومترات",
        "wh": "أدخل رقم رأس العين",
        "ut": "حالة الفحص",
        "remarks": "ملاحظات (اختياري)",
        "techs": "اختر الفنيين",
        "add_btn": "إضافة النشاط",
        "clear_btn": "مسح القائمة",
        "preview": "معاينة الرسالة (تم إضافة {count} من الأنشطة)",
        "final_msg": "الرسالة النهائية المجمعة",
        "send_wa": "إرسال عبر الواتساب",
        "empty": "القائمة فارغة حالياً. قم بتعبئة البيانات في الأعلى ثم اضغط على إضافة النشاط لتتمكن من إنشاء الرسالة.",
        "success_toast": "تم حفظ النشاط بنجاح.",
        "clear_toast": "تم مسح جميع الأنشطة.",
        "toggle_lang": "English",
        "toggle_theme": "الوضع النهاري" if st.session_state.theme == "Dark" else "الوضع الليلي",
        "save": "حفظ",
        "cancel": "إلغاء",
        "edit_btn": "تعديل النشاط",
        "modify_title": "تعديل النشاط"
    }
}

t = translations[st.session_state.lang]

# 4. Themes & Corporate Colors
direction = "rtl" if st.session_state.lang == "AR" else "ltr"
text_align = "right" if st.session_state.lang == "AR" else "left"

if st.session_state.theme == "Dark":
    bg_color = "#0F172A"
    text_color = "#F8FAFC"
    input_bg = "#1E293B"
    btn_bg = "#1E293B"
    btn_text = "#F8FAFC"
    btn_border = "#334155"
    tag_bg = "#334155"     
    tag_text = "#38BDF8"   
    card_bg = "#1E293B"
    accent_color = "#38BDF8"
else:
    bg_color = "#F1F5F9"  
    text_color = "#0F172A"  
    input_bg = "#FFFFFF"  
    btn_bg = "#FFFFFF"
    btn_text = "#0F172A"
    btn_border = "#CBD5E1"  
    tag_bg = "#EFF6FF"     
    tag_text = "#1E40AF"   
    card_bg = "#FFFFFF"
    accent_color = "#2563EB"

custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Base Reset and Padding Reduction */
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {bg_color} !important;
        font-family: 'Inter', sans-serif !important;
        direction: {direction};
    }}
    
    .block-container {{
        max-width: 650px !important;
        padding-top: 15px !important;
        padding-bottom: 20px !important;
    }}
    
    /* Solid Fixed Rectangle Frame (App Card) */
    .main-wrapper-box {{
        background-color: {card_bg};
        border: 1px solid {btn_border};
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-top: 5px;
    }}
    
    /* Labels and Headings Formatting */
    label p, .stRadio label, div[role="radiogroup"] label, [data-testid="stWidgetLabel"] p {{
        color: {text_color} !important;
        font-family: 'Inter', sans-serif !important;
        text-align: {text_align};
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-bottom: 2px !important;
    }}
    
    .main-title {{
        color: {accent_color} !important;
        text-align: center !important;
        font-size: 24px !important;
        font-weight: 700;
        margin-top: 0px;
        margin-bottom: 15px;
        letter-spacing: -0.5px;
    }}
    
    /* Perfect Alignment Harmony for Selectbox & Inputs */
    div[data-baseweb="input"], div[data-baseweb="select"], .stSelectbox div, .stTextInput input, .stNumberInput input, .stMultiSelect div {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {btn_border} !important;
        border-radius: 6px !important;
        height: 40px !important;
    }}
    
    /* Multi-Select Tags Fix */
    div[data-baseweb="tag"] {{
        background-color: {tag_bg} !important;
        border-radius: 4px !important;
        height: 26px !important;
    }}
    div[data-baseweb="tag"] * {{
        color: {tag_text} !important;
        fill: {tag_text} !important;
    }}
    
    /* Standardized Buttons Touch Targets */
    div.stButton > button {{
        background-color: {btn_bg} !important;
        color: {btn_text} !important;
        border: 1px solid {btn_border} !important;
        border-radius: 6px !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
        width: 100% !important;
        height: 42px !important;
        font-size: 14px !important;
    }}
    div.stButton > button:hover {{
        border-color: {accent_color} !important;
        color: {accent_color} !important;
    }}
    
    /* Primary (WhatsApp) Button styling */
    div.stButton > button[kind="primary"] {{
        background-color: {accent_color} !important;
        color: #FFFFFF !important;
        border: none !important;
        height: 46px !important;
    }}

    /* Compact Top Row Control Bars */
    div[data-testid="stHorizontalBlock"]:has(.top-ctrl-lang) {{
        direction: ltr !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: flex-start !important;
        gap: 6px !important;
        margin-bottom: 0px !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.top-ctrl-lang) div[data-testid="column"] {{
        width: max-content !important;
        flex: none !important;
    }}
    
    div[data-testid="column"]:has(.top-ctrl-lang) button,
    div[data-testid="column"]:has(.top-ctrl-theme) button {{
        min-width: 90px !important;
        height: 34px !important;
        font-size: 13px !important;
        padding: 0 8px !important;
        border-radius: 6px !important;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 5. Top Controls Row (Compact & clean)
col_lang, col_theme, _ = st.columns([1, 1, 12])

with col_lang:
    st.markdown('<span class="top-ctrl-lang"></span>', unsafe_allow_html=True)
    if st.button(t["toggle_lang"], key="lang_btn"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()

with col_theme:
    st.markdown('<span class="top-ctrl-theme"></span>', unsafe_allow_html=True)
    if st.button(t["toggle_theme"], key="theme_btn"):
        st.session_state.theme = "Dark" if st.session_state.theme == "Light" else "Light"
        st.rerun()

# Open Wrapper Frame Box
st.markdown('<div class="main-wrapper-box">', unsafe_allow_html=True)

st.markdown(f"<h1 class='main-title'>{t['title']}</h1>", unsafe_allow_html=True)

# --- 6. Callbacks ---
def add_activity_callback():
    act_type = st.session_state.line_type_key
    if st.session_state.remarks_key:
        ut_line = f"UT {st.session_state.ut_key} {st.session_state.remarks_key}"
    else:
        ut_line = f"UT {st.session_state.ut_key}"
        
    techs_list = "/".join(st.session_state.tech_key) if st.session_state.tech_key else "N/A"
    
    if act_type == "TL":
        line_val = st.session_state.line_key.replace("Line ", "")
        km_display = str(st.session_state.km_key) if st.session_state.km_key != 0.0 else "0"
        single_activity = f"{act_type} {line_val} km {km_display}\n {ut_line}\nTech : {techs_list}"
    elif act_type == "OSI":
        area_val = st.session_state.line_key
        wh_display = str(st.session_state.wh_key) if "wh_key" in st.session_state else "0"
        single_activity = f"{area_val}-{wh_display} OSI\n {ut_line}\nTech : {techs_list}"
    else:
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

st.radio(t["act_type"], ["TL", "OSI", "Other"], horizontal=True, key="line_type_key")

if st.session_state.line_type_key == "TL":
    if "line_key" in st.session_state and st.session_state.line_key not in [f"Line {i}" for i in range(1, 13)]:
        st.session_state.line_key = "Line 1"
    st.selectbox(t["line_num"], [f"Line {i}" for i in range(1, 13)], key="line_key")
    st.number_input(t["km"], value=0.0, min_value=0.0, step=0.001, format="%g", key="km_key")

elif st.session_state.line_type_key == "OSI":
    if "line_key" in st.session_state and st.session_state.line_key not in ["KHRS", "ABJF", "MZLJ"]:
        st.session_state.line_key = "KHRS"
    st.selectbox(t["area"], ["KHRS", "ABJF", "MZLJ"], key="line_key")
    st.number_input(t["wh"], value=0, min_value=0, step=1, key="wh_key")

else:
    st.text_input(t["custom_act"], key="custom_act_key")

st.radio(t["ut"], ["completed", "Not completed"], horizontal=True, key="ut_key")
st.text_input(t["remarks"], key="remarks_key")
st.multiselect(t["techs"], ["SKT", "SAN", "NAA", "NBO", "HSQ", "HAK", "IAS", "FLC"], key="tech_key")

st.markdown("<br>", unsafe_allow_html=True)

# --- 8. Action Buttons ---
col1, col2 = st.columns(2)
with col1:
    st.button(t["add_btn"], use_container_width=True, type="secondary", on_click=add_activity_callback)
with col2:
    st.button(t["clear_btn"], use_container_width=True, on_click=clear_all_callback)

st.markdown("---")

# --- 9. Preview and Send Section ---
if st.session_state.activities_list:
    st.markdown(f"### {t['preview'].format(count=len(st.session_state.activities_list))}")
    
    for i, activity in enumerate(st.session_state.activities_list):
        if st.session_state.get(f"editing_{i}", False):
            st.text_area(f"{t['modify_title']} {i+1}", value=activity, key=f"act_input_{i}")
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button(t["save"], key=f"save_{i}"):
                    st.session_state.activities_list[i] = st.session_state[f"act_input_{i}"]
                    st.session_state[f"editing_{i}"] = False
                    st.rerun()
            with col_cancel:
                if st.button(t["cancel"], key=f"cancel_{i}"):
                    st.session_state[f"editing_{i}"] = False
                    st.rerun()
        else:
            st.code(activity, language="text")
            if st.button(f"{t['edit_btn']} {i+1}", key=f"edit_btn_{i}"):
                st.session_state[f"editing_{i}"] = True
                st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            
    st.markdown("---")
    all_activities_joined = "\n\n".join(st.session_state.activities_list)
    final_whatsapp_text = f"Hello Activities today \n\n{all_activities_joined}"
    
    st.markdown(f"### {t['final_msg']}")
    st.code(final_whatsapp_text, language="text")
    
    encoded_message = urllib.parse.quote(final_whatsapp_text)
    whatsapp_url = f"https://wa.me/?text={encoded_message}"
    st.link_button(t["send_wa"], whatsapp_url, use_container_width=True, type="primary")
else:
    st.info(t["empty"])

# Close Wrapper Frame Box
st.markdown('</div>', unsafe_allow_html=True)

