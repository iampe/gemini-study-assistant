
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓"
)

st.title("🎓 AI Study Assistant")
st.caption("Ask questions and continue the conversation.")

# 1. Read the API key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is not configured.")
    st.stop()

# 2. Create the Gemini client
client = genai.Client(api_key=api_key)

# 3. Initialize chat history only once per session
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Start a new conversation
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# 5. Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Input for the next question
question = st.chat_input("Ask your next question...")

if question:
    if len(question) > 4000:
        st.warning("Please keep your question under 4000 characters.")
    else:
        # Save and display the user's question
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        try:
            # Build conversation history for Gemini
            history = []

            for message in st.session_state.messages:
                history.append({
                    "role": (
                        "user"
                        if message["role"] == "user"
                        else "model"
                    ),
                    "parts": [{"text": message["content"]}]
                })

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=history
                    )

                answer = response.text or "No text response returned."
                st.markdown(answer)

            # Save the assistant's answer
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as error:
            # Keep technical details out of the public interface
            print("Gemini request failed:", type(error).__name__)
            st.error(
                "Unable to generate a response. "
                "Check your API key, model access, connection, "
                "and usage limits."
            )
