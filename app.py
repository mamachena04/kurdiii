import os
from google import genai
from dotenv import load_dotenv

# 1. بارکردنی کلیلی نهێنی لە فایلی .env
load_dotenv()
API_KEY = os.getenv("AIzaSyDwz_P2bHwZGKczqMBmSGd3OnAaccV7erM")

# 2. پێکهێنانی کلاینتی Gemini
client = genai.Client(api_key=API_KEY)

# 3. دیاریکردنی مۆدێل (باشترین مۆدێل بۆ وەرگێڕان)
# بۆ وەرگێڕان، مۆدێلەکانی Gemini 1.5 Flash یان Pro زۆر باشن
MODEL_NAME = "gemini-1.5-flash"  # یان "gemini-1.5-pro"

# 4. فانکشنی وەرگێڕان
def translate_turkish_to_sorani(file_path):
    """
    فایلێکی تورکی دەخوێنێتەوە و دەیگێڕێتە سەر کوردی سۆرانی.
    """
    # خوێندنەوەی فایل
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            turkish_text = f.read()
        print(f"⏳ فایلەکە خوێندرایەوە: {file_path}")
    except FileNotFoundError:
        return "پەیامی هەڵە: فایلەکە نەدۆزرایەوە. تکایە ڕێڕەوی ڕاست بنووسە."

    # دروستکردنی پرۆمپتی وەرگێڕان (ئەم بەشە زۆر گرنگە بۆ وەرگێڕانێکی پاراو)
    prompt = f"""
    You are a professional translator specializing in Turkish to Central Kurdish (Sorani) translation.

    Your task is to translate the following Turkish text into **fluent, natural, and meaningful Sorani Kurdish**.

    Translation Guidelines:
    - Do NOT provide a word-for-word translation.
    - The output must sound like it was originally written in Sorani Kurdish.
    - Use proper Sorani grammar, vocabulary, and idioms.
    - Preserve the original meaning, tone, and style of the text.

    Turkish Text:
    {turkish_text}

    Sorani Kurdish Translation:
    """

    # ناردنی داواکاری بۆ Gemini
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        translation = response.text
        print("✅ وەرگێڕان بە سەرکەوتوویی ئەنجام درا.")
        return translation
    except Exception as e:
        return f"پەیامی هەڵە: کێشەیەک ڕوویدا لە پەیوەندیکردن بە Gemini - {str(e)}"

# 5. بەکارهێنان (مەین پرۆگرام)
if __name__ == "__main__":
    # ڕێڕەوی فایلە تورکییەکەت لێرە دابنێ
    input_file = "turkish_document.txt"  # ئەمە بە ناوی فایلەکەی خۆت بگۆڕە
    output_file = "sorani_translation.txt"

    # بانگکردنی فانکشنی وەرگێڕان
    translated_text = translate_turkish_to_sorani(input_file)

    # پاشەکەوتکردنی وەرگێڕانەکە لە فایلێکی نوێدا
    if not translated_text.startswith("پەیامی هەڵە"):
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated_text)
        print(f"📁 وەرگێڕانەکە پاشەکەوت کرا لە: {output_file}")
    else:
        print(translated_text)  # هەڵەکە پیشان بدە
