import streamlit as st
import requests
import os

# Ensure the 'uploads' directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Streamlit UI
st.title("Chat with Your File")

uploaded_file = st.file_uploader("Upload a File", type=["txt", "pdf", "docx"])
if uploaded_file is not None:
    # Save the uploaded file
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Send file to FastAPI for embedding
    with st.spinner("Processing the file..."):
        response = requests.post("http://localhost:8000/upload", files={"file": open(file_path, "rb")})
        if response.status_code == 200:
            st.success("File processed successfully!")
        else:
            st.error("Failed to process the file.")

    # Chat interaction
    st.subheader("Chat with your file")
    user_input = st.text_input("Ask something:")
    
    if user_input:
        chat_response = requests.post("http://localhost:8000/chat", json={"query": user_input})
        if chat_response.status_code == 200:
            st.write("Response:", chat_response.json()['answer'])
        else:
            st.error("Failed to get a response.")
