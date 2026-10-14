import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓"
)

st.title("🎓 AI Study Assistant")
st.write("Ask an educational question.")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API key is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)

level = st.selectbox(
    "Student level",
    ["School", "College", "University"]
)

style = st.selectbox(
    "Answer style",
    [
        "Simple explanation",
        "Example-based explanation",
        "Exam-oriented answer"
    ]
)

question = st.text_area("Enter your question")

if st.button("Generate Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    elif len(question) > 4000:
        st.warning("Please shorten your question.")
    else:
        prompt = f"""
        You are a helpful educational assistant.
        Student level: {level}
        Answer style: {style}
        Question: {question}

        Explain clearly and use examples when useful.
        """

        try:
            with st.spinner("Generating answer..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

            if response.text:
                st.subheader("Answer")
                st.markdown(response.text)
            else:
                st.warning("No text response was returned.")

        except Exception as error:
            # Keep the detailed error out of the public interface.
            print("Gemini request failed:", type(error).__name__)
            st.error(
                "Request failed. Check the model, API key, "
                "connection and usage limits."
            )
