import streamlit as st
import time
import datetime
from openai import OpenAI

st.set_page_config(page_title="StudyBuddy AI", page_icon="🤖", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.stButton > button {
    background: linear-gradient(90deg, #667eea, #764ba2);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

input, textarea, select {
    border-radius: 10px !important;
}

h1, h2, h3 {
    color: #f5f5f5;
}
</style>
""", unsafe_allow_html=True)

if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY not found in Streamlit Secrets")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "paused" not in st.session_state:
    st.session_state.paused = False

def typing_effect(text):
    placeholder = st.empty()
    typed = ""
    for char in text:
        typed += char
        placeholder.markdown(f"💬 {typed}")
        time.sleep(0.02)

def ai_response(prompt):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        return response.output_text
    except Exception:
        return "⚠️ AI temporarily unavailable. Stay focused, you’re doing great 💪"

if not st.session_state.logged_in:
    st.title("🤖 StudyBuddy AI")
    st.subheader("Your Personal Tutor & Study Manager")

    name = st.text_input("Enter your name")

    if st.button("Login"):
        if name.strip() != "":
            st.session_state.username = name
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.warning("Please enter your name")

else:
    st.title(f"👋 Hi {st.session_state.username}")
    st.subheader("Let’s study smart, not hard 💡")

    st.divider()
    st.subheader("⏰ Study Alarm")

    alarm_time = st.time_input("Select study start time")

    if st.button("Set Alarm"):
        st.success(f"Alarm set for {alarm_time}")

        now = datetime.datetime.now().time()
        while now < alarm_time:
            time.sleep(1)
            now = datetime.datetime.now().time()

        st.balloons()
        st.warning("⏰ Time to Study! Let’s go 💪")

    st.divider()
    st.subheader("📖 Start Study Session")

    subject = st.selectbox("Select Subject", ["Physics", "Maths", "Chemistry", "Biology"])
    duration = st.selectbox("Study Duration (minutes)", [30, 45, 60])
    mood = st.selectbox("Current Mood", ["Normal", "Lazy", "Stressed"])

    if st.button("Start Session"):
        prompt = f"""
        You are StudyBuddy AI, a friendly personal tutor.
        Teach {subject} in simple language.
        Ask 2 MCQ questions in between.
        Motivate the student if they feel {mood}.
        Keep it engaging and short.
        """

        st.success("📘 Study Session Started")
        text = ai_response(prompt)
        typing_effect(text)
        
        st.info("⏳ Study in progress")
        progress = st.progress(0)
        for i in range(100):
            if st.session_state.paused:
                st.warning("⏸️ Session Paused")
                break
            time.sleep((duration * 60) / 100)
            progress.progress(i + 1)

        if not st.session_state.paused:
            st.success("✅ Session Completed!")
            st.balloons()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏸️ Pause"):
            st.session_state.paused = True
    with col2:
        if st.button("▶️ Resume"):
            st.session_state.paused = False

    st.divider()
    st.subheader("💬 Chat with StudyBuddy")

    user_msg = st.text_input("Ask a doubt or share how you feel")

    if st.button("Send Message"):
        chat_prompt = f"""
        You are StudyBuddy AI, an emotional and motivational study friend.
        Help the student clearly and kindly.
        Student says: {user_msg}
        """

        reply = ai_response(chat_prompt)
        typing_effect(reply)

    st.toast("🔥 Keep going! Consistency wins.", icon="🚀")
