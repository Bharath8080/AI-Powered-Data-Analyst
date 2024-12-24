import os
import pandas as pd
import streamlit as st
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq

# Retrieve the API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the ChatGroq model with the environment variable API key
llm = ChatGroq(model_name="llama3-70b-8192", api_key=GROQ_API_KEY)

def main():
    st.set_page_config(page_title="Data Analyst Bot", page_icon="🤖", layout="centered")

    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f5f5;
        }
        h1 {
            color: #4CAF50;
            text-align: center;
        }
        .stFileUploader {
            text-align: center;
        }
        .stTextInput {
            text-align: center;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("DATA ANALYST - BOT")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", help="Upload your Excel file here.")

    if uploaded_file is not None:
        try:
            # Load data from the uploaded Excel file
            df = pd.read_excel(uploaded_file)
            st.write("Data Preview:")
            st.dataframe(df)  # Display the entire dataframe

            # Initialize SmartDataframe with the loaded data and LLM configuration
            sdf = SmartDataframe(df, config={"llm": llm})

            # Only show the question input if the file is successfully loaded
            question = st.text_input("Ask a question about your data:")

            if question:
                try:
                    response = sdf.chat(question)
                    st.write("Answer:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error processing the data with SmartDataframe: {e}")
        except Exception as e:
            st.error(f"Error reading the Excel file: {e}")

if __name__ == "__main__":
    main()
