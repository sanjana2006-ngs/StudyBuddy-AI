import streamlit as st
import time
import os
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

st.set_page_config(page_title="StudyBuddy AI", page_icon="🤖")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "paused" not in st.session_state:
    st.session_state.paused = False

if not st.session_state.logged_in:
    st.title("🤖 StudyBuddy AI")
    name = st.text_input("Enter your name to continue")

    if st.button("Login"):
        st.session_state.logged_in = True
        st.session_state.username = name
        st.rerun()

else:
    st.title(f"📚 Welcome {st.session_state.username}")
    st.subheader("Your Personal Tutor & Study Manager")

    subject = st.selectbox("📖 Select Subject", ["Physics", "Maths", "Chemistry", "Biology"])
    duration = st.selectbox("⏱️ Study Duration (minutes)", [30, 45, 60])
    mood = st.selectbox("😊 Current Mood", ["Normal", "Lazy", "Stressed"])

    if st.button("Start Study Session"):
        prompt = f"""
        You are StudyBuddy AI, a friendly tutor.
        Explain {subject} in a simple way.
        Ask 2 MCQ questions in between.
        Motivate if the student feels {mood}.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        st.success("📘 Study Session Started")
        st.write(response.choices[0].message.content)

        st.info("⏳ Study Timer Started")
        for i in range(duration * 60):
            if st.session_state.paused:
                st.warning("⏸️ Paused")
                break
            time.sleep(1)

        st.success("✅ Study Session Completed")

    if st.button("⏸️ Pause Session"):
        st.session_state.paused = True

    if st.button("▶️ Resume Session"):
        st.session_state.paused = False

    st.divider()

    st.subheader("💬 Chat with StudyBuddy")
    user_msg = st.text_input("Ask your doubt or say how you feel")

    if st.button("Send"):
        chat_prompt = f"""
        You are a motivational AI study buddy.
        Respond politely and helpfully.
        User says: {user_msg}
        """

        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": chat_prompt}]
        )

        st.write("🤖 StudyBuddy:", chat_response.choices[0].message.content)
