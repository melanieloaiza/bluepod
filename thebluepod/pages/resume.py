import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader, PdfFileReader
import os

from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from style import css

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def split_text(user_information):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=2000)
    docs = text_splitter.create_documents([user_information])
    return docs

def load_LLM(openai_api_key):
    llm = ChatOpenAI(temperature=.7,
                     openai_api_key=openai_api_key,
                     max_tokens=2000,
                     model_name='gpt-4')
    return llm


load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YourAPIKeyIfNotSet')

response_types = {
    'Resume Analysis': f"""
        Your task is to compile a list of 5-point feedback on the resume provided below. 
        Evaluate aspects such as Clarity, Content Relevance, Language, Achievements, Formatting, and Overall Impression. 
        Additionally, create a Chronological Resume Style for the candidate . 
        Submit your response in a concise paragraph, including all corrections and an example of the revised resume.
    """,
    'Cover Letter': f"""
        Your task is create a cover letter , one-page document that introduces resume person to the hiring manager, 
        expands upon the information in the uploaded resume and explains why is the best fit for job position .
    """
}

st.set_page_config(page_title="bluepod", page_icon="🦕")

st.markdown(css, unsafe_allow_html=True)
st.markdown('<div class="gradient-text"> ~ Resume Analysis</div>', unsafe_allow_html=True)

option = st.radio("Select an option:", ("Resume Analysis", "Cover Letter"))
if option == "Resume Analysis":
    st.info('📌 Instructions : \n\n  '
            'Please upload your most recent resume in PDF format for evaluation. Additionally, ensure you enter your full name in the "User Info" field provided.')
    user_info = st.text_input(label="User info", placeholder="e.g., Melanie Loaiza")
    pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Start'", accept_multiple_files=True,
                                key="pdf_docs")

    if st.button("Start"):
        output_type = "Resume Analysis"
        with st.spinner("Loading"):
            raw_text = ""
            for pdf in pdf_docs:
                raw_text += get_pdf_text([pdf])

            user_information_docs = split_text(raw_text)
            text_chunks = get_text_chunks(raw_text)
            vectorstore = get_vectorstore(text_chunks)
            st.session_state.conversation = get_conversation_chain(vectorstore)
            llm = load_LLM(openai_api_key=OPENAI_API_KEY)

            map_prompt = f"""
                You are a helpful AI bot that aids a user in research.
                Below is information about a person job position {user_info}.
                Information will include tweets, interview transcripts, and blog posts about {user_info}.
                Use specifics from the research when possible.

                {response_types[output_type]}

                % START OF INFORMATION ABOUT {user_info}:
                {{text}}
                % END OF INFORMATION ABOUT {user_info}:

                YOUR RESPONSE:
            """
            map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "user_info"])

            combine_prompt = f"""
                You are a helpful AI bot that aids a user in research.
                You will be given information about {user_info}.
                Do not make anything up, only use information which is in the person's context.

                {response_types[output_type]}

                % PERSON CONTEXT
                {{text}}

                % YOUR RESPONSE:
            """
            combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text", "user_info"])

            chain = load_summarize_chain(llm,
                                         chain_type="map_reduce",
                                         map_prompt=map_prompt_template,
                                         combine_prompt=combine_prompt_template)

            output = chain({"input_documents": user_information_docs, "text": raw_text})

            st.markdown(f"#### Output:")
            st.write(output['output_text'])

            # Add button to download formatted TXT
            st.download_button(
                label="Download TXT",
                data=output['output_text'],
                file_name="chronological_resume.txt",
                mime="text/plain"
            )
else:
    st.info('📌 Instructions : \n\n  '
            'Please upload your most recent resume in PDF format; this will serve as the basis for creating the cover letter. Additionally, ensure you enter the job title you are applying for in the designated field. '
            )
    job_info = st.text_input(label="Job title", placeholder="e.g., Data Analyst")
    job_infopdf = st.file_uploader("Upload your PDFs here and click on 'Start'", accept_multiple_files=True,
                                   key="job_infopdf")

    if st.button("Start"):
        output_type = "Cover Letter"
        response_text = response_types[output_type]
        with st.spinner("Loading"):
            raw_text = ""
            for pdf in job_infopdf:
                raw_text += get_pdf_text([pdf])

            user_information_docs = split_text(raw_text)
            text_chunks = get_text_chunks(raw_text)
            vectorstore = get_vectorstore(text_chunks)
            st.session_state.conversation = get_conversation_chain(vectorstore)
            llm = load_LLM(openai_api_key=OPENAI_API_KEY)

            map_prompt = f"""
                You are a helpful AI bot that aids a user in research.
                Below is information about a person job position {job_info}.
                Information will include tweets, interview transcripts, and blog posts about {job_info}.
                Use specifics from the research when possible.

                {response_text}  # Use the variable to inject the correct response text

                % START OF INFORMATION ABOUT {job_info}:
                {{text}}
                % END OF INFORMATION ABOUT {job_info}:

                YOUR RESPONSE:
            """
            map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "job_info"])

            combine_prompt = f"""
                You are a helpful AI bot that aids a user in research.
                You will be given information about {job_info}.
                Do not make anything up, only use information which is in the person's context.

                {response_text}  # Use the variable to inject the correct response text

                % PERSON CONTEXT
                {{text}}

                % YOUR RESPONSE:
            """
            combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text", "job_info"])

            # Note: Ensure that the 'chain' function is correctly receiving the required variables.
            chain = load_summarize_chain(llm,
                                         chain_type="map_reduce",
                                         map_prompt=map_prompt_template,
                                         combine_prompt=combine_prompt_template)

            output = chain({"input_documents": user_information_docs, "text": raw_text})

            st.markdown(f"#### Output:")
            st.write(output['output_text'])

            # Add button to download formatted TXT
            st.download_button(
                label="Download TXT",
                data=output['output_text'],
                file_name="Cover letter.txt",
                mime="text/plain"
            )