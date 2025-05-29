import streamlit as st
import requests
import pyttsx3

st.set_page_config(page_title="AI Market Brief", layout="centered")
st.title("Asia Tech Morning Brief")

# UI Button
if st.button("Run Morning Brief"):
    with st.spinner("Collecting data from agents..."):

        try:
            # 1. Call orchestrator agent
            orchestrated_data = requests.get("http://localhost:8003/morning_brief").json()

            # 2. Call language agent (Gemini)
            response = requests.post("http://localhost:8004/generate_summary", json=orchestrated_data)
            result = response.json()
            summary = result.get("summary")

            if summary:
                st.success("Summary generated!")
                st.markdown(f"**Summary:**\n\n{summary}")

                # 3. Speak the summary
                engine = pyttsx3.init()
                engine.setProperty('rate', 160)
                engine.say(summary)
                engine.runAndWait()
            else:
                st.error("No summary returned.")

        except Exception as e:
            st.error(f"Error: {str(e)}")
