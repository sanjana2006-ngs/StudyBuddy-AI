import streamlit as st
import time
import datetime
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="StudyBuddy AI", page_icon="🤖")

# ---------------- STYLES ----------------
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
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "paused" not in st.session_state:
    st.session_state.paused = False

# ---------------- AI SETUP ----------------
USE_AI = False
client = None

if "OPENAI_API_KEY" in st.secrets:
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        USE_AI = True
    except Exception:
        USE_AI = False

# ---------------- FUNCTIONS ----------------
def typing_effect(text):
    placeholder = st.empty()
    typed = ""
    for c in text:
        typed += c
        placeholder.markdown(f"💬 {typed}")
        time.sleep(0.02)

def ai_or_offline(prompt):
    if USE_AI:
        try:
            r = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )
            return r.output_text
        except Exception:
            pass

    # 🔁 OFFLINE FALLBACK (ALWAYS WORKS)
    return """
📘 Let's study together!

🔹 Explanation:
This topic is very important. Focus on understanding the basics first.

📝 MCQ 1:
What is force?
a) Energy  
b) Push or pull ✅  
c) Speed  
d) Work  

📝 MCQ 2:
SI unit of force is?
a) Joule  
b) Pascal  
c) Newton ✅  
d) Watt  

💪 You're doing great! Stay consistent.
"""

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:
    st.title("🤖 StudyBuddy AI")
    st.subheader("Your Personal Tutor & Study Manager")

    name = st.text_input("Enter your name")

    if st.button("Login"):
        if name.strip():
            st.session_state.logged_in = True
            st.session_state.username = name
            st.rerun()
        else:
            st.warning("Please enter your name")

# ---------------- MAIN APP ----------------
else:
    st.title(f"👋 Hi {st.session_state.username}")
    st.subheader("Let’s study smart 💡")

    if USE_AI:
        st.success("✅ AI Online Mode")
    else:
        st.warning("⚠️ Offline Demo Mode (AI fallback)")

    # ---------- ALARM ----------
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

    # ---------- STUDY SESSION ----------
    st.divider()
    st.subheader("📖 Study Session")

    subject = st.selectbox("Subject", ["Physics", "Maths", "Chemistry", "Biology"])
    duration = st.selectbox("Duration (minutes)", [30, 45, 60])
    mood = st.selectbox("Mood", ["Normal", "Lazy", "Stressed"])

    if st.button("Start Session"):
        prompt = f"""
        You are StudyBuddy AI.
        Teach {subject}.
        Ask 2 MCQs.
        Motivate student feeling {mood}.
        """

        st.success("📘 Session Started")
        typing_effect(ai_or_offline(prompt))

        progress = st.progress(0)
        for i in range(100):
            if st.session_state.paused:
                st.warning("⏸️ Paused")
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

    # ---------- CHATBOT ----------
    st.divider()
    st.subheader("💬 Chat with StudyBuddy")

    user_msg = st.text_input("Ask a question or say how you feel")

    if st.button("Send"):
        chat_prompt = f"Motivate and help the student. Student says: {user_msg}"
        typing_effect(ai_or_offline(chat_prompt))

    st.toast("🔥 Keep going! You got this!", icon="🚀")
