import streamlit as st
from query_db import ask_question  # Import your backend function

st.set_page_config(page_title="Lottery Chatbot", page_icon="🎰")
st.title("Lottery Chatbot")

question = st.text_input("Ask a question about the lottery:")
if question:
    with st.spinner("Thinking..."):
        answer = ask_question(question)
    st.success(answer)