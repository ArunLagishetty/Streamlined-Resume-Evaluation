import streamlit as st
import os
# File to save the data
filename = "candidate_job_info.txt"

def save_info(candidate_info, job_description):
    with open(filename, "w") as file:
        file.write(candidate_info + '\n')
        file.write(job_description + '\n')

def page_input_information():
    st.title("Enter Information")

    candidate_info = st.text_area("Enter Candidate Information")
    job_description = st.text_area("Enter the Job Description")

    if st.button("Submit"):
        if candidate_info and job_description:
            save_info(candidate_info, job_description)
            st.success("Information saved successfully. You can now run the interview application.")
            os.system('streamlit run final.py')
        else:
            st.error("Please enter both candidate information and a job description.")

page_input_information()
