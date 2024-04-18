from langchain_community.chat_models  import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from langchain.document_loaders import YoutubeLoader
from style import css
import streamlit as st

import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YourAPIKeyIfNotSet')

def load_LLM(openai_api_key):
    llm = ChatOpenAI(temperature=.7,
                     openai_api_key=openai_api_key,
                     max_tokens=2000,
                     model_name='gpt-4')
    return llm

def pull_from_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        text = md(text)
        return text if text else ""
    except Exception as e:
        st.error(f"Error pulling content from {url}: {e}")
        return ""

def get_video_transcripts(url):
    st.write("Getting YouTube Videos...")
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    documents = loader.load()
    transcript = ' '.join([doc.page_content for doc in documents])
    return transcript

def split_text(user_information):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000,
                                                   chunk_overlap=2000)
    docs = text_splitter.create_documents([user_information])
    return docs

response_types = {
    '5-Things you didnt know': """
        Your goal is to generate provide 5 important facts 
        Please respond with list of a few 5 facts based on the topics above
    """,
    'Summarize': """
        Your goal is to generate a 1 page summary about them
        Please respond with a few short paragraphs that would prepare someone to talk to this person
    """ ,
    'Sentiment Analysis':""" 
        Your goal is to classify the video as positive or negative 
        Bit explanation of why you consider the video positive or negative
        Please respond with the video sentiment as a positive or negative
    """ ,
    '3-Recommended videos': """ 
        Your goal is to recommend 3 similar youtube videos as the one uploaded . NO URLs needed
        Please respond with 3 similar videos recommended to watch 
    """
}

map_prompt = """You are a helpful AI bot that aids a user in research.
Below is information about a person named {persons_name}.
Information will include tweets, interview transcripts, and blog posts about {persons_name}
Use specifics from the research when possible

{response_type}

% START OF INFORMATION ABOUT {persons_name}:
{text}
% END OF INFORMATION ABOUT {persons_name}:

YOUR RESPONSE:"""
map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "persons_name", "response_type"])

combine_prompt = """
You are a helpful AI bot that aids a user in research.
You will be given information about {persons_name}.
Do not make anything up, only use information which is in the person's context

{response_type}

% PERSON CONTEXT
{text}

% YOUR RESPONSE:
"""

combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text", "persons_name", "response_type"])
st.set_page_config(page_title="bluepod", page_icon="🦕")

st.markdown(css, unsafe_allow_html=True)
st.markdown('<div class="gradient-text"> ~ Youtube: Beyond the Play Button</div>', unsafe_allow_html=True)

st.info('📌  Instructions : \n\n  '
            'Please paste the Youtube URL, then press the start button.  \n\n' )
with st.sidebar:
    output_type = st.radio(
        "Select an option:",
        ('Summarize', '5-Things you didnt know', '3-Recommended videos', 'Sentiment Analysis'))

person_name = st.text_input(label="Video category",  placeholder=" e.g., Vlogs, Tutorials, Documentaries ... ", key="persons_name")
youtube_videos = st.text_input(label="YouTube URLs (Use , to seperate videos)",  placeholder="e.g., https://www.youtube.com/watch?v=c_hO_fjmMnk", key="youtube_user_input")
def parse_urls(urls_string):
    return [url.strip() for url in urls_string.split(',')]
def get_content_from_urls(urls, content_extractor):
    return "\n".join(content_extractor(url) for url in urls)

button_ind = st.button("**Start**", type='secondary', help="Click to generate output based on information")

if button_ind:
    if not (youtube_videos):
        st.warning('Please provide links to parse', icon="⚠️")
        st.stop()

    video_text = get_content_from_urls(parse_urls(youtube_videos), get_video_transcripts) if youtube_videos else ""
    user_information = "\n".join([video_text])
    user_information_docs = split_text(user_information)

    llm = load_LLM(openai_api_key=OPENAI_API_KEY)
    chain = load_summarize_chain(llm,
                                 chain_type="map_reduce",
                                 map_prompt=map_prompt_template,
                                 combine_prompt=combine_prompt_template,
                                 )

    output = chain({"input_documents": user_information_docs,
                    "persons_name": person_name,
                    "response_type": response_types[output_type]
                    })

    st.markdown(f"#### Output:")
    st.write(output['output_text'])