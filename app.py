import streamlit as st
import pandas as pd
from datetime import datetime
import os

# اسم ملف قاعدة البيانات المؤقتة لـ حفظ الأنشطة
DATA_FILE = "ndt_activities.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["الفني", "الموقع/الخط", "نوع النشاط", "تفاصيل/رقم اللحام", "الوقت"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# إعدادات الصفحة لتكون متناسبة مع الشاشات
st.set_page_config(page_title="نظام تتبع أنشطة NDT", layout="wide")
st.title("📊 نظام تسجيل وتتبع أنشطة الفنيين والخطوط")

df_activities = load_data()

# تقسيم الشاشة إلى تبويبين للفني والمشرف
tab1, tab2 = st.tabs(["📝 تسجيل نشاط جديد", "📈 لوحة تحكم المشرف والتقارير"])

with tab1:
    st.header("تسجيل الأداء اليومي")
    
    with st.form("activity_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tech_name = st.text_input("اسم الفني / المفتش")
            line_id = st.text_input("رقم الخط / المشروع")
        with col2:
            activity_type = st.selectbox("نوع النشاط الحالي", [
                "فحص بالموجات فوق الصوتية (UT)",
                "إعداد وتجهيز الموقع (Setup)",
                "انتظار تصريح العمل (Standby - Permit)",
                "كتابة التقارير (Reporting)",
                "أخرى"
            ])
            details = st.text_area("تفاصيل إضافية (مثل: رقم اللحام Weld ID)")
            
        submit_btn = st.form_submit_button("تسجيل النشاط الحالي")
        
        if submit_btn and tech_name and line_id:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = pd.DataFrame([{
                "الفني": tech_name,
                "الموقع/الخط": line_id,
                "نوع النشاط": activity_type,
                "تفاصيل/رقم اللحام": details,
                "الوقت": current_time
            }])
            df_activities = pd.concat([df_activities, new_data], ignore_index=True)
            save_data(df_activities)
            st.success("تم تسجيل النشاط بنجاح!")

with tab2:
    st.header("متابعة الأنشطة والتقارير")
    
    if not df_activities.empty:
        st.dataframe(df_activities.sort_values(by="الوقت", ascending=False), use_container_width=True)
        
        csv = df_activities.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل التقرير اليومي كملف Excel/CSV",
            data=csv,
            file_name=f"NDT_Report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("لا توجد أنشطة مسجلة اليوم حتى الآن.")
