import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import requests

# Show title and description.
st.title("💬 MedWiseGPT")
st.write(
    "This is a simple chatbot that uses the Google Gemini API (1.5 Flash model) to generate responses."
)

# Ask user for their Google API key or service account JSON file.
google_api_key = st.text_input("Google API Key", type="password")
if not google_api_key:
    st.info("Please add your Google API key to continue.", icon="🗝️")
else:
    # Base URL for the Google Gemini API
    gemini_api_url = "https://gemini.googleapis.com/v1/models/gemini-1_5:generateText"

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare the request payload for Google Gemini API.
        payload = {
            "input": prompt,
            "context": [m["content"] for m in st.session_state.messages],
            "model": "gemini-1_5"
        }

        headers = {
            "Authorization": f"Bearer {google_api_key}",
            "Content-Type": "application/json"
        }

        try:
            # Make the API request to the Google Gemini service.
            response = requests.post(gemini_api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json().get("output", "No response from model.")

            # Display the response from the Gemini API.
            with st.chat_message("assistant"):
                st.markdown(result)
            st.session_state.messages.append({"role": "assistant", "content": result})
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
