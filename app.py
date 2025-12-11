import streamlit as st
import google.generativeai as genai

# 1. Configure the API Key
# We grab the API key from Streamlit Secrets (for security)
try:
    genai.configure(api_key=st.secrets["AIzaSyBaQs_Oz4IwaF-H7TqJ7hbnE4mFU-s6N3k"])
except Exception as e:
    st.error("API Key not found. Please set it in Streamlit Secrets.")

# 2. Set up the Model
# Paste the generation config from your AI Studio code here if you have specific settings
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

# Create the model
# NOTE: If you added a specific System Instruction in AI Studio (e.g., "You are an English Tutor"),
# add it inside the instruction="" quotes below.
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash", 
  generation_config=generation_config,
  system_instruction="You are a helpful and patient English language tutor. Correct grammar mistakes and help the user practice conversation."
)

# 3. Build the Streamlit App UI
st.title("English Tutoring Bot 🤖")
st.write("Start chatting to practice your English!")

# Initialize chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# 4. Handle User Input
if user_input := st.chat_input("Type your message here..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Save user message to history
    st.session_state.chat_history.append(("user", user_input))

    # Generate AI response
    try:
        # We start a chat session with history
        chat_session = model.start_chat(
            history=[
                {"role": role, "parts": [text]} 
                for role, text in st.session_state.chat_history 
                if role == "user" or role == "model" # Map user/model roles correctly
            ]
        )
        
        response = chat_session.send_message(user_input)
        ai_response = response.text

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        
        # Save AI response to history
        st.session_state.chat_history.append(("model", ai_response))

    except Exception as e:
        st.error(f"An error occurred: {e}")
