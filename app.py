import streamlit as st
import google.generativeai as genai
import re
import time

# --- ١. دیزاینی پڕۆفیشناڵ (HTML & CSS) ---
st.set_page_config(page_title="وەرگێڕی ژێرنووسی کوردی", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .main-container {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        height: 3.5em;
        font-size: 18px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- ٢. لۆجیکی وەرگێڕانی توند (Python) ---
def translate_text(text, model):
    if not text.strip() or text.isdigit():
        return text
    try:
        # ڕێنمایی زۆر توند بۆ ئەوەی مۆدێلەکە زمانی تورکی نەهێڵێتەوە
        prompt = f"""
        URGENT TASK: Translate the following subtitle text into KURDISH SORANI.
        
        STRICT RULES:
        1. OUTPUT ONLY the Kurdish Sorani translation.
        2. DELETE all Turkish or original words.
        3. Use natural, conversational Kurdish (Sorani).
        4. Do not explain anything, just give the translation.

        TEXT TO TRANSLATE: 
        {text}
        
        KURDISH SORANI:
        """
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return text
    except Exception:
        return text

# --- ٣. ڕووکاری بەکارهێنەر ---
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.title("🎬 وەرگێڕی ژێرنووسی زیرەک")
st.write("باشترین مۆدێلی ژیری دەستکرد بەکاردەهێنین بۆ وەرگێڕانی ژێرنووسەکانت بۆ کوردییەکی پاراو.")

# وەرگرتنی کلیل بە پارێزراوی
api_key = st.text_input("AIzaSyDwz_P2bHwZGKczqMBmSGd3OnAaccV7erM", type="password", help="ff")

uploaded_file = st.file_uploader("فایلی SRT هەڵبژێرە", type=['srt'])

if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    
    # بەکارهێنانی مۆدێلی Pro ئەگەر هەبێت بۆ مانای قووڵتر، ئەگەرنا Flash
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        # تاقیکردنەوەی مۆدێلەکە
        model.generate_content("hi")
    except:
        model = genai.GenerativeModel('gemini-1.5-flash')

    if st.button("🚀 دەستپێکردنی وەرگێڕانی کوردی"):
        raw_content = uploaded_file.getvalue().decode("utf-8")
        # جیاکردنەوەی بلۆکەکان بۆ ئەوەی کاتەکان تێکنەچن
        blocks = re.split(r'\n\s*\n', raw_content.strip())
        
        translated_srt = []
        progress_bar = st.progress(0)
        status_msg = st.empty()
        
        for i, block in enumerate(blocks):
            lines = block.split('\n')
            if len(lines) >= 3:
                index = lines[0]
                timestamp = lines[1]
                original_text = " ".join(lines[2:])
                
                # وەرگێڕان بە پڕۆمپتە نوێیەکە
                kurdish_text = translate_text(original_text, model)
                
                # دووبارە ڕێکخستنەوەی بلۆکەکە
                translated_srt.append(f"{index}\n{timestamp}\n{kurdish_text}")
                
                # نیشاندانی پێشکەوتن
                prog = (i + 1) / len(blocks)
                progress_bar.progress(prog)
                status_msg.text(f"وەرگێڕانی دێڕی {i+1} لە {len(blocks)}...")
                
                time.sleep(0.5) # پشوو بۆ API
        
        # دروستکردنەوەی ناوەڕۆکی کۆتایی
        final_output = "\n\n".join(translated_srt)
        
        st.success("✅ وەرگێڕان بە سەرکەوتوویی تەواو بوو!")
        st.download_button(
            label="📥 داگرتنی فایلی وەرگێڕدراو",
            data=final_output,
            file_name="kurdish_subtitle.srt",
            mime="text/plain"
        )
st.markdown("</div>", unsafe_allow_html=True)
