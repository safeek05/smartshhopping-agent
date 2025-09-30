import streamlit as st
import requests

# --- CONFIGURATION ---
# IMPORTANT: Replace with your actual n8n Webhook URL
# This is the URL you get from the n8n Webhook node (use the 'Production URL' for a deployed app)
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/0f99fc47-9e0b-4496-8132-b85a6c647127" 

# --- UI & STYLING ---

# Page configuration
st.set_page_config(
    page_title="Autonomous Shopping Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for a cleaner look
# Custom CSS for a cleaner look
def local_css():
    css = """
    <style>
        /* General styling */
        .stApp {
            background-color: #111827; /* Dark background */
            color: #ffffff; /* White text for readability */
        }
    ...
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# Apply the custom CSS
local_css()

# --- APP LAYOUT & LOGIC ---

# Header
st.title("🤖 Autonomous Shopping Assistant")
st.markdown("Tell me what you're looking for, and I'll find the best product for you, explain my choice, and find a discount.")

# Create a form for user input
with st.form(key="shopping_form"):
    user_request = st.text_area(
        label="Enter your shopping request:",
        placeholder="e.g., a comfortable office chair with good lumbar support under $250",
        height=100
    )
    
    submitted = st.form_submit_button(label="Find Best Product")

# --- HANDLE FORM SUBMISSION ---

if submitted:
    if not user_request:
        st.warning("Please enter a shopping request.")
    elif N8N_WEBHOOK_URL == "YOUR_N8N_WEBHOOK_URL_HERE":
        st.error("N8N Webhook URL is not configured. Please update the `N8N_WEBHOOK_URL` in the script.")
    else:
        # Show a spinner while the assistant is "thinking"
        with st.spinner("🤖 Assistant is on the job... Analyzing products and finding deals..."):
            try:
                # Send the user's request to the n8n workflow
                response_from_n8n = requests.post(
                    N8N_WEBHOOK_URL, 
                    json={"user_request": user_request}, 
                    timeout=90  # Set a timeout for the request
                )
                
                # Raise an exception for bad status codes (4xx or 5xx)
                response_from_n8n.raise_for_status()

                # Process the successful response
                result_data = response_from_n8n.json()
                assistant_summary = result_data.get("summary", "Sorry, I couldn't get a summary.")

                st.subheader("Assistant's Report:")
                st.markdown(f'<div class="result-box">{assistant_summary}</div>', unsafe_allow_html=True)
                st.success("Task completed!")

            except requests.exceptions.RequestException as e:
                # Handle network or HTTP errors
                st.error(f"Failed to communicate with the shopping assistant workflow. Please try again later. Error: {e}")
            except Exception as e:
                # Handle other potential errors (e.g., JSON parsing)
                st.error(f"An unexpected error occurred: {e}")

# Add a footer or instruction section
st.markdown("---")
st.info("This assistant uses AI to analyze products. The final purchase decision is yours. Always double-check product details on the merchant's website.")
