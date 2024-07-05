import time #Iwish
import os
import json
import requests
import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import google.generativeai as genai


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity - AI Google Ads Generator",
        layout="wide",
    )
    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }

        ::-webkit-scrollbar {
            width: 16px;
        }
        div.stButton > button:first-child {
            background: #1565C0;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
      </style>
    """
    , unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    st.title("Ultimate AI Google Ads Generator by Alwrity")
    st.write("Effortlessly create high-performing, optimized Google Ads with our AI-driven tool. Boost your campaign success today!")

    with st.expander("**💡 PRO-TIP** - Read the instructions below.", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            product_service_name = st.text_input("🏷️ Brand/Product/Service Name:")
        
            call_to_action_options = ["Shop Now", "Learn More", "Sign Up", "Get a Quote", "Download", "Custom"]
            call_to_action = st.selectbox("🔔 Call to Action:", call_to_action_options)
            if call_to_action == "Custom":
                call_to_action = st.text_input("🔔 Enter custom CTA:")
        
        with col2:
            key_benefit_usp = st.text_input("🔑 Keywords (Optional):")
        
        with col3:
            target_audience = st.text_input("🎯 Specify Target Audience:", placeholder="Specify Target Audience to attract")

    if st.button('**✍️ Write Google Ads Copy**'):
        with st.status("Assigning AI professional to write your Google Ads copy..", expanded=True) as status:
            if not product_service_name or not target_audience or not key_benefit_usp:
                st.error("🚫 Error: Enter all the details, least you can do..")
            else:
                response = google_ads_writer(product_service_name, call_to_action, key_benefit_usp, target_audience, status)
                if response:
                    st.subheader(f'**🧕🔬👩 Alwrity can make mistakes. Your Final Google Ads!**')
                    st.write(response)
                else:
                    st.error("💥**Failed to write Letter. Please try again!**")


def google_ads_writer(product_service_name, call_to_action, key_benefit_usp, target_audience, status):
    """ Email project_update_writer """

    prompt = f"""## Google Ads Description Generation Request

        **Product/Service:** {product_service_name}
        **Target Audience:** {target_audience}
        **Key Benefit/USP:** {key_benefit_usp}
        **Call to Action:** {call_to_action}
        
        ## Instructions for AI
        
        * Generate 5 compelling and concise Google Ads descriptions, each within the character limit (approximately 90 characters).
        * Highlight the key benefit/USP and tailor the message to the target audience.
        * Include a strong call to action (CTA) that aligns with the campaign goals.
        * Incorporate the Product/Service Name, ensuring it complements the ad copy.
        * Ensure ad descriptions are tailored for given Target Audience.
        * Focus on creating a sense of urgency and scarcity where appropriate.
        * Ensure ad descriptions are clear, specific, and easy to understand.
        * Maintain a consistent tone and style throughout the ad copy.
        * Consider using ad extensions for additional information and visibility.
        
        ## Output Format
        
        * Two separate ad descriptions, each on a new line.
        """
    status.update(label="Writing Google Ads Description...")
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        api_key (str): Your Google Generative AI API key.
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        generation_config = {
            "temperature": 0.6,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 1096,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()
