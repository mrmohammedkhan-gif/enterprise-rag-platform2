import streamlit as st
from rag import generate_answer

st.set_page_config(
    page_title="Enterprise RAG Assistant",
    layout="wide"
)

st.title("Enterprise RAG Evaluation & Observability Platform")
st.caption("Azure OpenAI • Azure AI Search • Vector Search • PDF RAG • Grounded Responses")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask an enterprise document question")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving documents and generating grounded answer..."):
            answer, docs = generate_answer(question)

        st.write(answer)

        with st.expander("Retrieved Context"):
            for i, doc in enumerate(docs, start=1):
                st.markdown(f"**Chunk {i}: {doc['source']}**")
                st.write(doc["content"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })