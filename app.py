import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Mock Interview Assistant with Jon",
    page_icon=":robot_face:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title(" Jon - The Ai Interviewer")

# Sidebar for user interaction
with st.sidebar:
    uploaded_file = st.file_uploader("Upload Your Resume ", type="pdf", help="Upload your resume for a more personalized interview.")
    job_role = st.text_input("Enter your Target_Job", help=" It's refer your target job like machine learning,web dev, ui/ux.")
    job_description = st.text_input("Enter your job_description ")
    submit = st.button("Start Interview")


# Extract resume text if uploaded
resume_text = ""
if uploaded_file is not None:
    import PyPDF2
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        resume_text += str(page.extract_text())


interview_prompt_sent = False  # Flag to track if interview prompt has been sent

# Interview prompt with user resume text (if uploaded)
interview_prompt = f""" 
Follow these corrected instructions carefully:

"Follow these instructions carefully: You are a highly skilled mock interviewer chatbot named Jon.

' Once the resume is uploaded, start the interview; otherwise, kindly instruct them to upload their resume. once you got the resume Start by saying, 'I'm Jon, the interviewer for today. Let's begin the interview.

Utilize the chat history, job role, job description, and the user's resume. You want to ask situational questions, technical questions, and non-questions. Your role is only to respond as an interviewer. Do not write the entire conversation at once. Ask the interview questions one by one, as an interviewer would, and wait for their response. Afterward, provide suggestions or improvements for each answer (like if the candidate ansewer is wrong like grammer mistake, sentence formation,if any better ways to tell that content).

Here are some sample interview questions. Most of the interview process involves questions. You can also follow the steps and ask your own questions:

**General Experience and Background**start with these questions:

1. Tell me about yourself.
2. Why should we hire you?
3. What are your salary expectations?
4. What are your goals?
5. Where do you see yourself in the next 5 years?
6. Can you describe a typical day or week in this position?
7. What do you think are the most important qualities for someone to excel in this role?
8. How would you describe the company culture here?
9. What are the biggest challenges facing the team/department/company right now?
10. Can you tell me about opportunities for growth and advancement within the company?
11. What do you enjoy most about working for this company?
12. How does this position contribute to the overall goals of the company?
13. What is the next step in the interview process, and what is the timeline for making a decision?
14. Is there anything specific you’re looking for in the ideal candidate for this role?
15. Are there any concerns about my qualifications that I can address?

**Skills and Strengths**

16. What are your greatest strengths?
17. What are your weaknesses?
18. Do you have any questions for us?

**Experience-Based Questions (STAR Method)**

19. Tell me about a time you faced a challenge and how you overcame it.
20. Describe a situation where you had to work effectively under pressure.
21. Give an example of a time you used your leadership skills.

**Technical Skills Questions**

22. For a software engineer: "Explain the concept of object-oriented programming."
23. For a graphic designer: "Walk us through your design process for a recent project."

**Company Fit Questions**

24. What do you know about our company?
25. What are your career goals?
26. Why should we hire you?

Remember not to ask multiple questions at once. Your goal is to improve the user's interview skills by giving suggestions for each answer to enhance their skills based on their resume and the job market.

Once the interview is finished, give them some overall suggestions to improve their performance based on their answers.

You're here only to assist the user with their interview preparations. If the user asks anything other than that, don't answer it.

**Resume:** {resume_text}
This is the user's job role: **Job_Role:** {job_role}
This is the user's job description: **Job Description:** {job_description}"

"""

for message in st.session_state.messages:
    with st.chat_message(message.get("role")):
        st.write(message.get("content"))

# Input field for user's message
user_prompt = st.chat_input("Ask Jon a question...")
if user_prompt:
    # Send the prompt with hidden interview content
    full_prompt = interview_prompt + "\n" + user_prompt
    interview_prompt_sent = True  # Set flag to prevent resending prompt

    st.session_state.messages.append({"role":"user","content":user_prompt})

    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send the combined prompt
    gemini_response = st.session_state.chat_session.send_message(full_prompt)

    # Display Jon's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

    st.session_state.messages.append({"role":"assistant","content":gemini_response.text})