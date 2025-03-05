from PIL import Image
import streamlit as st
import google.generativeai as genai

from configs import SYSTEM_PROMPT, SAFETY_SETTINGS, GENERATION_CONFIG, MODEL_NAME

if __name__ == '__main__':
    # Configure Model
    genai.configure(api_key="AIzaSyByxD3APIGmf1aA_PnTzR7jpl53FvUzwlk")
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        safety_settings=SAFETY_SETTINGS,
        generation_config=GENERATION_CONFIG,
        system_instruction=SYSTEM_PROMPT
    )

    # Setup Page
    st.set_page_config(page_title='تحليل الأشعة السينية - كشف الأمراض')
    st.title('تحليل الأشعة السينية')
    st.subheader('تحليل الأشعة السينية بالذكاء الاصطناعي - الإعداد: علي أمجد هادي.')

    # Body
    col1, col2 = st.columns([1, 5])
    submit_btn = col1.button('تحليل', use_container_width=True)
    uploaded_file = col2.file_uploader('رفع صورة الأشعة:', type=['png', 'jpg', 'jpeg', 'jfif'], accept_multiple_files=False)
    
    col3, col4 = st.columns(2)

    if uploaded_file:
        try:
            image_data = Image.open(uploaded_file).convert("RGB")  # تأكد من أن الصورة بصيغة RGB
            col3.image(image_data, use_column_width=True)  # عرض الصورة
            message = col4.chat_message("Model:")
        except Exception as e:
            st.error(f"خطأ في تحميل الصورة: {e}")
            image_data = None

    if submit_btn and uploaded_file:
        if image_data:
            # تحليل الصورة
            history = st.session_state.get('history', [])

            content = [
                "هذه صورة أشعة سينية لمريض. قم بتحليلها لاكتشاف أي أمراض محتملة، مثل الالتهاب الرئوي، الكسور، الأورام، السل، أمراض القلب أو أي حالات غير طبيعية أخرى. قدم تقريرًا طبيًا شاملًا.",
                image_data
            ]

            history.append({
                "role": "user",
                "parts": content,
            })

            chat_session = model.start_chat()
            response = chat_session.send_message(content)
            message.write(response.text)

            st.session_state['history'] = chat_session.history
        else:
            st.error("يرجى تحميل صورة صالحة قبل التحليل.")
