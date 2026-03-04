import streamlit as st
import google.generativeai as genai
import time

# کلیلەکەت لێرە دابنێ
genai.configure(api_key="AIzaSyA3xiFw-wAtwINwYQpnEDNV3OOLJrZKnoM")

st.set_page_config(page_title="وەرگێڕی ژێرنووسی پێشکەوتوو", layout="wide")
st.title("🎬 وەرگێڕی فایلی SRT (وەشانی جێگیر)")

SYSTEM_PROMPT = "Translate this SRT subtitle part to Kurdish Sorani. Keep timestamps and numbers exactly the same. Translate for meaning and natural flow. Output only SRT."

def split_srt(text, chunk_size=40): # قەبارەی پارچەکانمان بچووکتر کردەوە بۆ دڵنیایی زیاتر
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    for line in lines:
        current_chunk.append(line)
        if len(current_chunk) > chunk_size and line.strip() == "":
            chunks.append("\n".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    return chunks

uploaded_file = st.file_uploader("فایلی SRT لێرە دابنێ", type=['srt'])

if uploaded_file:
    srt_content = uploaded_file.getvalue().decode("utf-8")
    
    if st.button("دەستپێکردنی وەرگێڕان"):
        chunks = split_srt(srt_content)
        st.info(f"فایلەکە بە سەرکەوتوویی کرا بە {len(chunks)} پارچە.")
        
        full_translation = ""
        progress_bar = st.progress(0)
        
        # لێرە ناوی مۆدێلە جیاوازەکان تاقی دەکەینەوە
        model_names = ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-1.5-flash']
        
        success_model = None
        
        for i, chunk in enumerate(chunks):
            translated_chunk = None
            
            # هەوڵدان بۆ بەکارهێنانی مۆدێلەکان یەک لە دوای یەک تا دانەیەکیان کار دەکات
            for m_name in model_names:
                try:
                    model = genai.GenerativeModel(m_name)
                    response = model.generate_content(f"{SYSTEM_PROMPT}\n\n{chunk}")
                    translated_chunk = response.text
                    success_model = m_name # ئەگەر یەکێکیان کاری کرد، دەیکەینە مۆدێلی سەرەکی
                    break
                except:
                    continue
            
            if translated_chunk:
                full_translation += translated_chunk + "\n"
                progress = (i + 1) / len(chunks)
                progress_bar.progress(progress)
                time.sleep(2) # کاتی چاوەڕێمان زیاد کرد بۆ ئەوەی API بلۆکمان نەکات
            else:
                st.error(f"هەڵە لە پارچەی {i+1}: ناتوانرێت پەیوەندی بە Gemini بکرێت. تکایە دڵنیابەرەوە لە ئینتەرنێتەکەت یان کلیلەکەت.")
                break
        
        if full_translation:
            st.success("هەموو فایلەکە بە سەرکەوتوویی وەرگێڕدرا!")
            st.download_button("📥 داگرتنی فایلی وەرگێڕدراو", full_translation, file_name="kurdish_subtitle.srt")