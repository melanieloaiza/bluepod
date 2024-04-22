from langchain_community.chat_models  import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import YoutubeLoader

import streamlit as st
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from style import css
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
        Your goal is to provide five important facts about user_information_docs.  Add the importance of the videos_category
        Please respond with a list of five key facts based on the topics discussed above
    """,
    'Summarize': """
        Your task is to generate a one-page summary based on the provided user_information_docs. 
        After reviewing the summary, please compose four short paragraphs. 
        These paragraphs should effectively prepare someone for a discussion or presentation related to this video. 
        The goal is to ensure that the individual is well-informed and ready to engage meaningfully with the content.
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
Below is information about a video category {videos_category}.
Information will include all the information relate to the video {videos_category}
Use specifics from the research when possible

{response_type}

% START OF INFORMATION ABOUT {videos_category}:
{text}
% END OF INFORMATION ABOUT {videos_category}:

YOUR RESPONSE:"""
map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "videos_category", "response_type"])

combine_prompt = """
You are a helpful AI bot that aids a user in research.
You will be given information about {videos_category}.
Do not make anything up, only use information which is in the video's context

{response_type}

% VIDEO CONTEXT
{text}

% YOUR RESPONSE:
"""

combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text", "videos_category", "response_type"])
st.set_page_config(page_title="bluepod", page_icon="🦕")

st.markdown(css, unsafe_allow_html=True)
st.markdown('<div class="gradient-text"> ~ Youtube: Beyond the Play Button</div>', unsafe_allow_html=True)

st.info('📌  Instructions : \n\n  '
            'Please paste the Youtube URL, then press the start button.  \n\n' )
with st.sidebar:
    output_type = st.radio(
        "Select an option:",
        ('Summarize', '5-Things you didnt know', '3-Recommended videos', 'Sentiment Analysis'))

video_category = st.text_input(label="Video category",  placeholder=" e.g., Vlogs, Tutorials, Documentaries ... ", key="videos_category")
youtube_videos = st.text_input(label="YouTube URL",  placeholder="e.g., https://www.youtube.com/watch?v=c_hO_fjmMnk", key="youtube_user_input")
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
                    "videos_category": video_category,
                    "response_type": response_types[output_type]
                    })

    st.markdown(f"#### Output:")
    st.write(output['output_text'])