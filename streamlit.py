import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize Groq client
llm_client = Groq()

# App title and configuration
st.set_page_config(
    page_title="Interview Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define available topics
topics = ["Finance", "Marketing", "Analytics", "Operations"]

# Custom CSS for enhanced UI
def inject_custom_css():
    st.markdown("""
    <style>
        .element-container .stButton .st-emotion-cache-ocsh0s{   
            float:right;
        }
        .st-emotion-cache-t1wise{
            padding:1rem 10rem;
            width:70%;
        }
        label{
            display:none;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    inject_custom_css()
    
    # Title and header
    st.markdown(f'<h1 class="main-title">🤖 Interactive Interview Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Get expert answers to your professional questions</p>', unsafe_allow_html=True)
    
    # Topic selection in a styled container
    st.markdown('<div class="content-card topic-selector">', unsafe_allow_html=True)
    topic = st.selectbox("🌍 Choose your expertise area:", topics, index=0)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area in a styled container
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    user_input = st.text_area("", placeholder="Type your question here...", height=120)
    
    if st.button("🔎 Get Expert Answer"):
        if user_input.strip() == "":
            st.warning("⚠️ Please enter a question.")
        else:
            get_response(topic, user_input)
    
    st.markdown('</div>', unsafe_allow_html=True)

def get_response(topic, user_input):
    system_prompt = f"""
    You are a highly knowledgeable and experienced AI specializing in {topic}.
    Your role is to provide clear, accurate, and detailed answers exclusively related to {topic}.
    If a user poses a question about {topic}, respond with your best expertise.
    However, if the user asks about any subject outside of {topic}, reply with: 
    'Sorry, I cannot answer that. Feel free to ask me anything about {topic}.'
    """
    
    # Response container
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<h3>💡 Generated Response:</h3>", unsafe_allow_html=True)
    
    with st.spinner("⏳ Generating response..."):
        try:
            llm_response = llm_client.chat.completions.create(
                model='llama-3.3-70b-versatile',
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                stream=True
            )
            
            response_text = ""
            response_container = st.empty()
            
            for chunk in llm_response:
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content
                    response_container.markdown(f'<div class="response-container">{response_text}</div>', unsafe_allow_html=True)
                    time.sleep(0.05)
            
            st.markdown('<div class="success-message">✅ Response generated successfully!</div>', unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
