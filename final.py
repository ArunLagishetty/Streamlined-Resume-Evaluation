import streamlit as st
from bardapi import BardCookies, Bard

filename = "candidate_job_info.txt"

# Function to load information
def load_info():
    with open(filename, "r") as file:
        candidate_info = file.readline().strip()
        job_description = file.readline().strip()
    return candidate_info, job_description

# Function to generate questions using Bard
def generate_question_with_bard(candidate_info, job_description):
    cookie_dict = {
    "__Secure-1PSID": "fAg2u32UgcoZmxRtDokRrQ7-a1zVT9MVjvPBOkjMQG9kjsPCsAhiNK_ZTQSovhb0HUuOqA.",
    "__Secure-1PSIDTS": "sidts-CjEBPVxjSnulJW_CwilZFizL-xgI1F0TAC4qq_3W1TiuG-Lr9hU3FC_0NyT_3NTQAGOwEAA",
    "__Secure-1PSIDCC": "ABTWhQEIKkOFlMKlWXVqemvU0a0RmCR0ik12J0OmsR731dYjSM2YmpMvfeetkhns6-LIn0SHaU7p",
    # Any cookie values you want to pass session object.
}

    bard = BardCookies(cookie_dict=cookie_dict)
    prompt = f"For the candidate information '{candidate_info}',act as a interviewer and ask a single question for the job description '{job_description} keep the response short and crisp'"
    response = bard.get_answer(prompt)
    return response['content']

# Load candidate information and job description
candidate_info, job_description = load_info()

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_question = 0
    st.session_state.questions = []
    st.session_state.answers = []

st.title("Interview Questions")

# Display current question and input field for the answer
if st.session_state.current_question >= len(st.session_state.questions):
    new_question = generate_question_with_bard(candidate_info, job_description)
    st.session_state.questions.append(new_question)

current_question = st.session_state.questions[st.session_state.current_question]
st.subheader(f"Question {st.session_state.current_question + 1}")
st.write(current_question)
answer = st.text_input("Your Answer:")

# Buttons for navigating questions
col1, col2 = st.columns(2)
with col1:
    if st.button("Next Question"):
        if answer:
            st.session_state.answers.append(answer)
            st.session_state.current_question += 1
            st.experimental_rerun()
        else:
            st.warning("Please provide an answer before moving to the next question.")

with col2:
    if st.button("End Test"):
        if answer:
            st.session_state.answers.append(answer)
        st.session_state.test_completed = True
        st.experimental_rerun()

# Displaying all questions and answers after test is ended
if st.session_state.get("test_completed", False):
    st.title("Test Summary")
    for i, (question, answer) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
        st.subheader(f"Question {i+1}")
        st.write(question)
        st.subheader("Your Answer")
        st.write(answer)

    if st.button("Start Over"):
        st.session_state.clear()
        st.experimental_rerun()
