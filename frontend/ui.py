import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/classify"

st.set_page_config(page_title="Log Classifier", layout="centered")

st.title("Log Classifier Demo")

st.markdown("Paste raw logs below and classify them.")

log_input = st.text_area(
    "Logs",
    height=250,
    placeholder="2024-06-01 12:00:00 - User logged in\n2024-06-01 12:05:00 - Disk full"
)

if st.button("Classify"):
    if not log_input.strip():
        st.warning("Please enter logs.")
    else:
        with st.spinner("Classifying..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"raw": log_input},  # Important
                    timeout=15,
                )

                if response.status_code == 200:
                    st.success("Done")
                    st.json(response.json())
                else:
                    st.error(f"Error {response.status_code}")
                    st.json(response.json())

            except Exception as e:
                st.error(f"Request failed: {e}")