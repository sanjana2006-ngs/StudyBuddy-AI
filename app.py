import streamlit as st
import datetime
from openai import OpenAI

# Initialize client
client = OpenAI(api_key="YOUR_API_KEY")

st.set_page_config(page_title="StudyGenie", page_icon="📚")

st.title("📚 StudyGenie – AI Study Reminder & Motivation Bot")

# User Inputs
subject = st.text_input("📖 Subject")
study_time = st.time_input("⏰ Study Time")
mood = st.selectbox("😊 Current Mood", ["Lazy", "Stressed", "Normal"])

if st.button("Get AI Reminder"):
    prompt = f"""
    Create a short motivational study reminder.
    Subject: {subject}
    Mood: {mood}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    st.success("🔔 Study Reminder")
    st.write(response.choices[0].message.content)

st.divider()

# Chatbot Section
st.subheader("💬 Motivation Chatbot")
user_msg = st.text_input("Talk to your AI study buddy")

if st.button("Send"):
    chat_prompt = f"""
    You are a friendly AI study motivation coach.
    Respond empathetically and positively.
    Student says: {user_msg}
    """

    chat_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": chat_prompt}]
    )

    st.write("🤖 AI:", chat_response.choices[0].message.content)
