import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("RAG App Prototype")

# Upload section
uploaded_file = st.file_uploader("Upload a document", type=["txt"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    with st.spinner("Uploading..."):
        res = requests.post(f"{BACKEND_URL}/upload-document", files=files)

    if res.status_code == 200:
        st.success(res.json())
    else:
        st.error(f"Backend error: {res.status_code}")
        st.text(res.text)

st.write("---")

# Query section
st.subheader("Ask a question:")
query = st.text_input("Your question:")

if st.button("Submit Query"):
    with st.spinner("Thinking..."):
        res = requests.post(
            f"{BACKEND_URL}/query",
            json={"query": query}
        )

    if res.status_code == 200:
        st.json(res.json())
    else:
        st.error(f"Backend error: {res.status_code}")
        st.text(res.text)
