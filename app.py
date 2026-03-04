import streamlit as st
from google import genai
import os

# ڕێکخستنی پەڕە
st.set_page_config(page_title="وەرگێڕی تورکی بۆ کوردی (سۆرانی)", page_icon="🌐")
st.title("🌐 وەرگێڕی تورکی بۆ کوردی سۆرانی")
st.markdown("فایلێکی تورکی هەڵبژێرە بۆ وەرگێڕان بۆ کوردیی سۆرانی (پاراو و پڕمانا)")

# وەرگرتنی کلیلی ئەی پی ئای لە نهێنییەکان (Secrets)
try:
    API_KEY = st.secrets["AIzaSyDwz_P2bHwZGKczqMBmSGd3OnAaccV7erM"]
except Exception:
    st.error("❌ کلیلی ئەی پی ئای نەدۆزرایەوە. تکایە لە ڕێکخستنەکانی ئەپەکەتدا GOOGLE_API_KEY دابنێ.")
    st.stop()

# پێکهێنانی کلاینتی Gemini
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-1.5-flash"  # یان "gemini-1.5-pro"

# بەشی هەڵگرتنی فایل
uploaded_file = st.file_uploader("📁 فایلی تورکی هەڵبژێرە (txt, pdf, docx)", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    # خوێندنەوەی ناوەڕۆکی فایل
    try:
        # بۆ فایلی txt
        if uploaded_file.type == "text/plain":
            turkish_text = uploaded_file.read().decode("utf-8")
        else:
            # بۆ جۆرەکانی تر (pdf, docx) پێویستە کتێبخانەی زیادە دابمەزرێنیت
            st.warning("پاڵپشتی تەنها بۆ فایلی txt لەم نموونەیەدا هەیە. بۆ pdf یان docx پێویستە کتێبخانەی وەک PyPDF2 یان python-docx زیاد بکەیت.")
            st.stop()
        
        st.success("✅ فایل بە سەرکەوتوویی خوێندرایەوە.")
    except Exception as e:
        st.error(f"هەڵە لە خوێندنەوەی فایل: {e}")
        st.stop()

    # دروستکردنی پرۆمپتی وەرگێڕان
    prompt = f"""
    You are a professional translator specializing in Turkish to Central Kurdish (Sorani) translation.

    Translate the following Turkish text into **fluent, natural, and meaningful Sorani Kurdish**.

    Translation Guidelines:
    - Do NOT provide a word-for-word translation.
    - The output must sound like it was originally written in Sorani Kurdish.
    - Use proper Sorani grammar, vocabulary, and idioms.
    - Preserve the original meaning, tone, and style.

    Turkish Text:
    {turkish_text}

    Sorani Kurdish Translation:
    """

    # دوگمەی وەرگێڕان
    if st.button("🚀 وەرگێڕان"):
        with st.spinner("تکایە چاوەڕێ بە... وەرگێڕان ئەنجام دەدرێت."):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )
                translation = response.text

                # پیشاندانی وەرگێڕان
                st.subheader("📄 وەرگێڕانەکە:")
                st.write(translation)

                # دانەیەک بۆ دابگرتن
                st.download_button(
                    label="💾 دابگرتن وەک فایلی txt",
                    data=translation.encode("utf-8"),
                    file_name="sorani_translation.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"هەڵە لە وەرگێڕان: {e}")
