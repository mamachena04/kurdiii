import streamlit as st
import google.generativeai as genai
import re
import time

# --- ١. ڕێکخستنی ڕووکار (CSS & HTML) ---
st.set_page_config(page_title="وەرگێڕی ژێرنووسی پڕۆ", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stApp {
        background-color: #f4f7f6;
    }
    .main-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(45deg, #2193b0, #6dd5ed);
        color: white;
        border: none;
        height: 3em;
        font-weight: bold;
    }
    .progress-text {
        color: #555;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ٢. لۆجیکی وەرگێڕان (Python) ---
def translate_block(text, model):
    if not text.strip() or text.isdigit():
        return text
    try:
        prompt = f"وەک وەرگێڕێکی پیشەگەر، ئەم دەقە بە زمانی کوردییەکی زۆر پاراو و سروشتی سۆرانی بنووسەوە. تەنها وەرگێڕانەکە بنووسە:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else text
    except Exception:
        return text

# --- ٣. پێکهاتەی وێبسایتەکە ---
st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.title("🎬 وەرگێڕی ژێرنووسی زیرەک")
st.write("فایلی SRT باربکە و بە مۆدێلی Gemini وەریگێڕە بۆ کوردی.")

# وەرگرتنی کلیل بە شێوەی پاسۆرد بۆ پارێزراوی
api_key = st.text_input("AIzaSyDwz_P2bHwZGKczqMBmSGd3OnAaccV7erM", type="password", help="ffff")

uploaded_file = st.file_uploader("هەڵبژاردنی فایلی SRT", type=['srt'])

if uploaded_file and api_key:
    # ڕێکخستنی مۆدێل
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if st.button("🚀 دەستپێکردنی وەرگێڕانی پاراو"):
        # خوێندنەوەی فایل
        raw_content = uploaded_file.getvalue().decode("utf-8")
        # جیاکردنەوەی بلۆکەکان بەبێ تێکدانی کاتەکان
        blocks = re.split(r'\n\s*\n', raw_content.strip())
        
        translated_srt = []
        progress_bar = st.progress(0)
        status = st.empty()
        
        for i, block in enumerate(blocks):
            lines = block.split('\n')
            if len(lines) >= 3:
                index = lines[0]
                timestamp = lines[1]
                text = " ".join(lines[2:])
                
                # وەرگێڕانی تەنها دەقەکە
                kurdish_text = translate_block(text, model)
                
                # دروستکردنەوەی بلۆکەکە
                translated_srt.append(f"{index}\n{timestamp}\n{kurdish_text}")
                
                # نوێکردنەوەی پێشکەوتن
                prog = (i + 1) / len(blocks)
                progress_bar.progress(prog)
                status.markdown(f"<p class='progress-text'>خەریکی چارەسەرکردنی دێڕی {i+1} لە {len(blocks)}...</p>", unsafe_allow_html=True)
                
                # پشوو بۆ پاراستنی API
                time.sleep(0.6)
        
        # یەکخستنەوەی فایلەکە
        final_output = "\n\n".join(translated_srt)
        
        st.success("✅ وەرگێڕان بە سەرکەوتوویی تەواو بوو!")
        st.download_button(
            label="📥 داگرتنی فایلی وەرگێڕدراو",
            data=final_output,
            file_name="translated_kurdish.srt",
            mime="text/plain"
        )
st.markdown("</div>", unsafe_allow_html=True)
