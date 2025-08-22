import streamlit as st
from app.common import logger
from app.common.custom_exception import CustomException
from app.config.settings import settings
import requests

logger=logger.get_logger(__name__)

st.set_page_config(page_title=f"Multi AI Agent")
st.title("Multi AI Agent")

system_prompt=st.text_area("Define your AI Agent",height=70)
ai_model=st.selectbox("Select your AI model",options=settings.ALLOWED_MODEL_NAMES)
allow_web_search=st.checkbox("Allow web search")
user_input=st.text_input("Write your query")
API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_input:
    payload = {
        "model_name": ai_model,
        "system_prompt": system_prompt,
        "message": [user_input],
        "allow_search": allow_web_search
    }

    try:
        logger.info("Sending request to backend")
        response = requests.post("http://127.0.0.1:9999/chat", json=payload, timeout=60)

        response.raise_for_status()  # Raises exception for 4xx/5xx

        # Check response
        agent_response = response.json().get("response", "")
        logger.info("Successfully received response from backend")
        st.subheader("Agent Response")
        st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        st.error(f"Failed to communicate with backend: {e}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        st.error(f"Unexpected error occurred: {e}")
