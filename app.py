import streamlit as st
import google.generativeai as genai
from audio_recorder_streamlit import audio_recorder

# 1. Configure the API Key
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found. Please set it in Streamlit Secrets.")

# 2. Configure the Model (Gemini 1.5 Flash handles Audio!)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # We update the instructions to specifically listen for pronunciation
  system_instruction="You are an English Tutor. Listen to the user's audio. If they make pronunciation errors, correct them gently. If they speak clearly, continue the conversation naturally in English. Keep responses concise."
)

st.title("English Tutor with Voice 🎙️")
st.write("Click the microphone to speak. The AI will listen and correct your pronunciation!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, content in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(content)

# 3. Add the Microphone
# This creates a button. Click to record, click again to stop.
audio_bytes = audio_recorder(text="", icon_size="2x")

if audio_bytes:
    # Display what the user just sent (audio player)
    with st.chat_message("user"):
        st.audio(audio_bytes, format="audio/wav")
    
    # Add a placeholder to show the user we sent the audio
    st.session_state.chat_history.append(("user", "🎤 [Sent Audio Message]"))

    # 4. Send Audio to Gemini
    try:
        # Gemini expects a dictionary for audio parts
        response = model.generate_content([
            "Please analyze my pronunciation and respond to what I said.",
            {"mime_type": "audio/wav", "data": audio_bytes}
        ])
        
        ai_response = response.text

        # Display AI Response
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        
        # Save to history
        st.session_state.chat_history.append(("model", ai_response))

    except Exception as e:
        st.error(f"Error analyzing audio: {e}")

# Optional: Keep text input if they want to type
if user_input := st.chat_input("Or type your message here..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))
    
    response = model.generate_content(user_input)
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.chat_history.append(("model", response.text))
