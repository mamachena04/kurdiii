import streamlit as st
import google.generativeai as genai
import re
import time
from io import BytesIO

# --- ١. دیزاین و ڕووکار (HTML & CSS) ---
st.set_page_config(page_title="وەرگێڕی ژێرنووسی کوردی", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    .status-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #ffffff;
        border-right: 5px solid #007bff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- ٢. لۆجیکی وەرگێڕان (Python & AI) ---
def translate_text(text, model):
    if not text.strip() or text.isdigit(): return text
    try:
        # ڕێنمایی ورد بۆ وەرگێڕانی ماناگرا
        prompt = f"وەک وەرگێڕێکی فیلم، ئەم دەقە بە کوردییەکی زۆر پاراو و سروشتی سۆرانی بنووسەوە. تەنها وەرگێڕانەکە بنووسە:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else text
    except:
        return text

# --- ٣. ڕووکاری وێبسایتەکە ---
st.title("🎬 وەرگێڕی ژێرنووسی پڕۆفیشناڵ")
st.write("فایلی ژێرنووسەکەت لێرە دابنێ بۆ وەرگێڕانێکی پاراو و بێ کێشە لە کاتەکان.")

api_key = st.text_input("AIzaSyDwz_P2bHwZGKczqMBmSGd3OnAaccV7erM", type="password")

uploaded_file = st.file_uploader("هەڵبژاردنی فایلی SRT", type=['srt'])

if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if st.button("🚀 دەستپێکردنی وەرگێڕان"):
        content = uploaded_file.getvalue().decode("utf-8")
        blocks = re.split(r'\n\s*\n', content.strip())
        
        translated_content = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, block in enumerate(blocks):
            lines = block.split('\n')
            if len(lines) >= 3:
                index = lines[0]
                timestamp = lines[1]
                text = " ".join(lines[2:])
                
                # وەرگێڕانی دەقەکە
                kurdish_text = translate_text(text, model)
                
                # دووبارە دروستکردنەوەی بلۆکەکە
                translated_content.append(f"{index}\n{timestamp}\n{kurdish_text}")
                
                # نوێکردنەوەی ڕێژەی پێشکەوتن
                progress = (i + 1) / len(blocks)
                progress_bar.progress(progress)
                status_text.markdown(f"<div class='status-box'>خەریکی وەرگێڕان: {i+1} لە {len(blocks)} دێڕ</div>", unsafe_allow_html=True)
                
                time.sleep(0.5) # بۆ ئەوەی API نەوەستێت
        
        final_srt = "\n\n".join(translated_content)
        
        st.success("✨ وەرگێڕان بە سەرکەوتوویی تەواو بوو!")
        st.download_button(
            label="📥 داگرتنی فایلی وەرگێڕدراو",
            data=final_srt,
            file_name="translated_kurdish.srt",
            mime="text/plain"
        )
