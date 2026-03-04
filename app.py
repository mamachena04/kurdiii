import streamlit as st
import google.generativeai as genai
import time

# 🔑 لێرە کلیلە نوێیەکەت دابنێ کە لە Google AI Studio دروستت کردووە
API_KEY = "AIzaSyDwz_P2bHwZGKczqMBmSGd3OnAaccV7erM"

# ڕێکخستنی مۆدێل
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"کێشە لە کلیلەکە هەیە: {e}")

# ڕێکخستنی لاپەڕە و ستایلی کوردی
st.set_page_config(page_title="وەرگێڕی ژێرنووس", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; }
    .stButton>button { width: 100%; background-color: #007bff; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 وەرگێڕی ژێرنووسی SRT بۆ کوردی")
st.write("فایلی SRT باربکە بۆ ئەوەی بە شێوەی ماناگرا بۆت وەربگێڕێت.")

# فرمانی وەرگێڕان بە سیستەمی تاقیکردنەوەی مۆدێلەکان
def translate_text(text):
    # لیستێک لە مۆدێلەکان ئەگەر یەکێکیان کاری نەکرد بچێتە سەر ئەوی تر
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
    
    prompt = f"Translate this SRT subtitle part to Kurdish Sorani. Keep timestamps and structure exactly as they are. Output only the SRT.\n\n{text}"
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except:
            continue
    return None

uploaded_file = st.file_uploader("فایلی SRT هەڵبژێرە", type=['srt'])

if uploaded_file:
    # خوێندنەوەی ناوەڕۆکی فایلەکە
    content = uploaded_file.getvalue().decode("utf-8")
    lines = content.split('\n')
    
    # دابەشکردن بۆ پارچەی ٤٠ دێڕی بۆ ئەوەی Free API بلۆکمان نەکات
    chunks = ["\n".join(lines[i:i + 40]) for i in range(0, len(lines), 40)]
    
    if st.button("🚀 دەستپێکردنی وەرگێڕان"):
        translated_full = ""
        progress_bar = st.progress(0)
        status = st.empty()
        
        for i, chunk in enumerate(chunks):
            status.text(f"وەرگێڕانی پارچەی {i+1} لە {len(chunks)}...")
            result = translate_text(chunk)
            
            if result:
                translated_full += result + "\n"
                progress_bar.progress((i + 1) / len(chunks))
                # پشوو بۆ ئەوەی Rate Limit دروست نەبێت
                time.sleep(1.5)
            else:
                st.error(f"هەڵە لە وەرگێڕانی پارچەی {i+1}. تکایە دڵنیابەرەوە لە کلیلەکەت.")
                break
        
        if translated_full:
            st.success("✅ وەرگێڕان بە سەرکەوتوویی تەواو بوو!")
            st.download_button(
                label="📥 داگرتنی فایلی وەرگێڕدراو",
                data=translated_full,
                file_name="translated_kurdish.srt",
                mime="text/plain"
            )
