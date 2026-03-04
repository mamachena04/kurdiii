import streamlit as st
import google.generativeai as genai
import time

# 🔑 کلیلە نوێیەکەت لێرە دابنێ
API_KEY = "AIzaSyDZTm888ebwmI81HmNkEn4m5TCbzWQhcy0"
genai.configure(api_key=API_KEY)

# ڕێکخستنی لاپەڕە
st.set_page_config(page_title="وەرگێڕی ژێرنووسی کوردی", layout="wide", initial_sidebar_state="collapsed")

# ستایلی RTL بۆ زمانی کوردی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; }
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 وەرگێڕی ژێرنووسی SRT بۆ کوردی")
st.info("ئەم وێبسایتە مۆدێلی Gemini بەکاردەهێنێت بۆ وەرگێڕانی فایلی SRT بە شێوەیەکی زیرەک.")

# سیستەمی وەرگێڕان
def translate_chunk(text, model_name="gemini-1.5-flash"):
    system_prompt = "You are a professional subtitle translator. Translate this SRT content to Kurdish Sorani. Keep timestamps exactly same. Output ONLY the translated SRT."
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(f"{system_prompt}\n\n{text}")
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# بەشی بارکردنی فایل
uploaded_file = st.file_uploader("فایلی SRT لێرە دابنێ", type=['srt'])

if uploaded_file:
    content = uploaded_file.getvalue().decode("utf-8")
    lines = content.split('\n')
    
    # دابەشکردنی فایلەکە بۆ پارچەی بچووک (بۆ ئەوەی Free API نەوەستێت)
    chunk_size = 40 
    chunks = ["\n".join(lines[i:i + chunk_size]) for i in range(0, len(lines), chunk_size)]
    
    if st.button("🚀 دەستپێکردنی وەرگێڕانی فایلەکە"):
        full_text = ""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, chunk in enumerate(chunks):
            status_text.text(f"خەریکی وەرگێڕانی پارچەی {i+1} لە {len(chunks)}...")
            translated = translate_chunk(chunk)
            
            if "Error" in translated:
                st.error(f"هەڵەیەک ڕوویدا لە پارچەی {i+1}. تکایە دڵنیابەرەوە لە کلیلەکەت.")
                break
            
            full_text += translated + "\n"
            progress_bar.progress((i + 1) / len(chunks))
            time.sleep(1.5) # چاوەڕوانی بۆ ڕێگری لە بلۆککردنی API
            
        if full_text:
            st.success("✅ وەرگێڕان بە سەرکەوتوویی کۆتایی هات!")
            st.download_button(
                label="📥 داگرتنی فایلی وەرگێڕدراو",
                data=full_text,
                file_name="translated_kurdish.srt",
                mime="text/plain"
            )