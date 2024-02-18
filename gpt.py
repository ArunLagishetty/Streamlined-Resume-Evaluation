import streamlit as st
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import textract  # For extracting text from resumes
from sklearn.feature_extraction.text import CountVectorizer
import os
import PyPDF2
import docx
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
import os
# Function to extract text from resume
def extract_text_from_resume(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        # Extract text from PDF
        with pdfplumber.open(file_path) as pdf:
            text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file_extension == '.docx':
        # Extract text from DOCX
        doc = docx.Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
    else:
        # Handle other file types as plain text
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()

    return text

# Function to extract keywords

def extract_keywords_tfidf(text, top_n=10):
    tfidf = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
    tfidf_matrix = tfidf.fit_transform([text])
    feature_array = tfidf.get_feature_names_out()
    tfidf_sorting = tfidf_matrix.toarray().flatten().argsort()[::-1]

    top_keywords = [feature_array[i] for i in tfidf_sorting[:top_n]]
    return top_keywords

# Function to generate questions
def generate_question(keywords, job_description, model_name='gpt2'):
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Create a more specific prompt
    prompt = f"Based on the resume keywords {', '.join(keywords)} and the job description '{job_description}', generate interview questions:"
    encoded_input = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(
        encoded_input, 
        max_length=100, 
        num_return_sequences=5, 
        num_beams=5,
        no_repeat_ngram_size=2
    )

    questions = [tokenizer.decode(o, skip_special_tokens=True) for o in output]
    return questions

from bardapi import BardCookies, Bard

# ... [rest of your imports and functions]

# Import Bard API
from bardapi import BardCookies, Bard
import streamlit as st
import random
import time

# Function to generate questions using Bard
def generate_question_with_bard(candidate_info, job_description):
    bard = BardCookies(token_from_browser=True)
    prompt = f"For the candidate information '{candidate_info}', give me only 1 single question to ask for an interview for the job description '{job_description}', act as a hr and ask do not reply as bard only give the question in the response do not say anything like Generating questions"
    response = bard.get_answer(prompt)
    return response['content']

st.title("Interview Question Generator Chat")

# Initialize chat history and state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.candidate_info = None
    st.session_state.job_description = None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
user_input = st.chat_input("PLEASE ENTER THE INFORMATION")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process input based on the state
    if not st.session_state.candidate_info:
        st.session_state.candidate_info = user_input
        assistant_response = "Thank you. Now, please enter the job description."
    elif not st.session_state.job_description:
        st.session_state.job_description = user_input
        assistant_response = "Generating interview questions based on the provided information..."
        # Generate questions using Bard
        questions = generate_question_with_bard(st.session_state.candidate_info, st.session_state.job_description)
        assistant_response += "\n" + questions
        # Reset the state for new queries
        st.session_state.candidate_info = None
        st.session_state.job_description = None
    else:
        assistant_response = "Please enter candidate information."

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)  # Add a delay to simulate typing
            message_placeholder.markdown(full_response + "▌")  # Simulate a blinking cursor
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
