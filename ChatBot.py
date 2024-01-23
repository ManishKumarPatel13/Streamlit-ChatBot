import textwrap
# from markdown import Markdown
from Apis import gemini_key
import google.generativeai as genai
import pyttsx3
import streamlit as st
from IPython.display import Markdown
# from IPython.display import display


# Configuring api 
api_key = gemini_key()
genai.configure(api_key=api_key)


# Function to convert text into markdown format
def to_markdown(text):
  text = text.replace('.', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# chat uses model as assistant so converting role
def role_to_streamlit(role):
  if role =="model":
    return "assistant"
  else:
    return role


# Initializing and Configuring model
model = genai.GenerativeModel(model_name='gemini-pro', safety_settings={'HARASSMENT' :'block_none', 'HATE_SPEECH':'block_none'})


# Initialazing chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history = [])

# Chat input area
prompt = st.chat_input(placeholder="Enter a prompt here")
# Generating response
if prompt:
    response = st.session_state.chat.send_message(prompt)
    print(response.text)
    try:
        mark = to_markdown(response.text).data
        # mark_space.write(response.text)
        for message in st.session_state.chat.history:
          with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(to_markdown(message.parts[0].text).data)
    except Exception as e:
        st.error("Something Went Wrong!!")
        
            
    
