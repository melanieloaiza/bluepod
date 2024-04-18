from langchain_community.chat_models  import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from Bio import Entrez
import pandas as pd
import numpy as np
import streamlit as st
import os
from dotenv import load_dotenv
from style import css

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YourAPIKeyIfNotSet')

def load_LLM(openai_api_key):
    llm = ChatOpenAI(temperature=.7,
                     openai_api_key=openai_api_key,
                     max_tokens=2000,
                     model_name='gpt-4')
    return llm
def split_text(split_information):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000,
                                                   chunk_overlap=2000)
    docs = text_splitter.create_documents([split_information])
    return docs
def search(query):
    Entrez.email = 'email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='pub+date',
                            retmax='1',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results
def search(query1):
    Entrez.email = 'email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='pub+date',
                            retmax='5',
                            retmode='xml',
                            term=query1)
    results = Entrez.read(handle)
    return results
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

response_types = {
                'README file' : """
                       Your goal is to create a README file individually for each research paper uploaded below
                       {df}
                       The README file should contain the following information :
                       1. General information :
                            1.1 Provide a title for the research paper
                            1.2 Name/institution/address/email information for Principal investigator (or person responsible for collecting the data)
                            1.3 Abstract information
                            1.4 Date of data collection (can be a single date, or a range)
                            1.5 Information about geographic location of data collection
                            1.6 Keywords used to describe the data topic
                            1.7 Information about funding sources that supported the collection of the data
                       2. For each filename, a short description of what data it contains
                       3. Date that the file was created
                       3. Licenses or restrictions placed on the data
                       4. Methodological information
                           4.1 Description of methods for data collection or generation (include links or references to publications or other documentation containing experimental design or protocols used)
                           4.2 Description of methods used for data processing (describe how the data were generated from the raw or collected data)
                           4.3 Any software or instrument-specific information needed to understand or interpret the data, including software and hardware version numbers
                           4.4 Standards and calibration information, if appropriate
                           4.5 key descriptive information about the experiment, (e.g. sampling or measurement methods, software used for analysis, any processing or transformations performed)
                        5. Results
                        Please keep the READFILE standard format . You can add more information that you find relevant for the README file.
                    """
}
map_prompt = """You are a helpful AI bot that aids a user in research.
Below is information about a person job position {query}.
Information will include tweets, interview transcripts, and blog posts about {query}
Use specifics from the research when possible

{response_type}

% START OF INFORMATION ABOUT {query}:
{text}
% END OF INFORMATION ABOUT {query}:

YOUR RESPONSE:"""
map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "query", "response_type" ])

combine_prompt = """
You are a helpful AI bot that aids a user in research.
You will be given information about {query}.
Do not make anything up, only use information which is in the person's context

{response_type}

% PERSON CONTEXT
{text}

% YOUR RESPONSE:
{df}
"""

combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text", "query", "response_type", "df"])

st.set_page_config(page_title="bluepod", page_icon="🦕")

st.markdown(css, unsafe_allow_html=True)
st.markdown('<div class="gradient-text"> ~ PubMeds Goldmine</div>', unsafe_allow_html=True)

option = st.radio("Select an option:", ("README file", "Research Paper Data Collection"))

if option == "README file":
        st.info('📌 Instructions : \n\n  ' 
                'Please enter the paper PMID (PubMed ID). '
                'You can locate the PMID at the bottom of the papers title on the PubMed official website (https://pubmed.ncbi.nlm.nih.gov) \n\n '
                '*This README file aims to provide comprehensive details about the research paper. If some of the information appears as blank, it means it was not presented in the papers data*.')
        query = st.text_input(label="PMID :  ", placeholder="e.g., 10789670 ")
        output_type = "README file"

        if query:
            split_information = query
            split_information_docs = split_text(split_information)

        if st.button("Search"):
            if query:
                studies = search(query)
                studies_id_list = studies.get('IdList', [])
                df_str = ""
                if studies_id_list:
                    papers = fetch_details(studies_id_list)
                    title_list = []
                    PMID = []
                    pubmedID = []
                    abstract_list = []
                    journal_list = []
                    language_list = []
                    pubdate_year_list = []
                    pubdate_month_list = []
                    author_list = []
                    affiliation_list = []
                    link_list = []
                    keyword_list = []
                    doi_list = []
                    pmid_list = []
                    funding_list = []
                    mesh_list = []
                    keyword_list = []

                    for i, paper in enumerate(papers['PubmedArticle']):
                        title_list.append(paper['MedlineCitation']['Article']['ArticleTitle'])
                        try:
                            abstract = paper['MedlineCitation']['Article']['Abstract']['AbstractText']
                            if isinstance(abstract, list):
                                abstract = ' '.join(abstract)
                        except KeyError:
                            abstract = 'No Abstract'
                        abstract_list.append(abstract)
                        journal_list.append(paper['MedlineCitation']['Article']['Journal']['Title'])
                        language_list.append(paper['MedlineCitation']['Article']['Language'][0])
                        try:
                            pubdate_year_list.append(paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year'])
                        except KeyError:
                            pubdate_year_list.append('No Data')
                        try:
                            pubdate_month_list.append(paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Month'])
                        except KeyError:
                            pubdate_month_list.append('No Data')

                        authors = paper['MedlineCitation']['Article']['AuthorList']
                        author_names = []
                        author_affiliations = []
                        for author in authors:
                            if 'LastName' in author:
                                full_name = author['LastName']
                                if 'ForeName' in author:
                                    full_name += ' ' + author['ForeName']
                                author_names.append(full_name)
                            if 'AffiliationInfo' in author and author['AffiliationInfo']:
                                author_affiliations.append(author['AffiliationInfo'][0]['Affiliation'])
                            else:
                                author_affiliations.append('No Affiliation')

                        author_list.append(', '.join(author_names))
                        affiliation_list.append('; '.join(author_affiliations))

                        pubmed_id = paper['MedlineCitation']['PMID']
                        link = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
                        link_list.append(link)

                        pubmed_id = paper['MedlineCitation']['PMID']
                        pubmedID.append(pubmed_id)

                        try:
                            keywords = paper['MedlineCitation']['KeywordList']
                            if keywords:
                                keyword_list.append(', '.join([keyword.strip() for keyword in keywords[0]]))
                            else:
                                keyword_list.append('No Keywords')
                        except KeyError:
                            keyword_list.append('No Keywords')

                        try:
                            funding_info = paper['MedlineCitation']['Article'].get('GrantList', [])
                            if funding_info:
                                grants = []
                                for grant in funding_info:
                                    grant_id = grant.get('GrantID', 'Unknown GrantID')
                                    agency = grant.get('Agency', 'Unknown Agency')
                                    grants.append(f"{grant_id} ({agency})")
                                funding_list.append('; '.join(grants))
                            else:
                                funding_list.append('No Funding Information')
                        except KeyError:
                            funding_list.append('No Funding Information')

                        try:
                            mesh_headings = paper['MedlineCitation']['MeshHeadingList']
                            mesh_descriptor_names = []
                            for mesh in mesh_headings:
                                descriptor_name = mesh['DescriptorName'].strip()
                                mesh_descriptor_names.append(descriptor_name)
                            mesh_list.append('; '.join(mesh_descriptor_names))
                        except KeyError:
                            mesh_list.append('No Mesh Headings')

                    df = pd.DataFrame({
                        'Title': title_list,
                        'PMID': pubmedID,
                        'Abstract': abstract_list,
                        'Journal': journal_list,
                        'Language': language_list,
                        'Year': pubdate_year_list,
                        'Month': pubdate_month_list,
                        'Authors': author_list,
                        'Affiliations': affiliation_list,
                        'Funding_Information': funding_list,
                        'Mesh_Headings': mesh_list,
                        'Link': link_list,
                        'Keywords': keyword_list
                    })

                    month_mapping = {
                        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
                        'No Data': np.nan
                    }
                    df['Month'] = df['Month'].replace(month_mapping)

                    df_str = df.to_string(index=False)

            llm = load_LLM(openai_api_key=OPENAI_API_KEY)
            chain = load_summarize_chain(llm,
                                                 chain_type="map_reduce",
                                                 map_prompt=map_prompt_template,
                                                 combine_prompt=combine_prompt_template,
                                                 )
            output = chain({"input_documents": split_information_docs,
                            "query": query,
                            "response_type": response_types[output_type],
                            "df": df_str
                            })

            st.write(output['output_text'])

            if output['output_text']:
                st.download_button(
                    label="Download Text File",
                    data=output['output_text'],
                    file_name="output.txt",
                    mime="text/plain"
                )
else:
    st.info('📌 Instructions : \n\n  '
            'Please enter either keywords or the main topic of your search. We will query the latest 5 papers from the PubMed website based on that. '
            )

    query1 = st.text_input(label="Subject / Keyword :  ", placeholder="e.g., Distance as a barrier to obstetric care among indigenous women in Panama ")
    if query1:
        split_information = query1
        split_information_docs = split_text(split_information)

    if st.button("Search"):
        if query1:
            studies = search(query1)
            studies_id_list = studies.get('IdList', [])
            df_str = ""
            if studies_id_list:
                papers = fetch_details(studies_id_list)

                title_list = []
                PMID = []
                pubmedID =[]
                abstract_list = []
                journal_list = []
                language_list = []
                pubdate_year_list = []
                pubdate_month_list = []
                author_list = []
                affiliation_list = []
                link_list = []
                keyword_list = []
                doi_list = []
                pmid_list = []
                funding_list = []
                mesh_list = []
                keyword_list = []

                for i, paper in enumerate(papers['PubmedArticle']):
                    title_list.append(paper['MedlineCitation']['Article']['ArticleTitle'])
                    try:
                        abstract = paper['MedlineCitation']['Article']['Abstract']['AbstractText']
                        if isinstance(abstract, list):
                            abstract = ' '.join(abstract)
                    except KeyError:
                        abstract = 'No Abstract'
                    abstract_list.append(abstract)
                    journal_list.append(paper['MedlineCitation']['Article']['Journal']['Title'])
                    language_list.append(paper['MedlineCitation']['Article']['Language'][0])
                    try:
                        pubdate_year_list.append(
                            paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year'])
                    except KeyError:
                        pubdate_year_list.append('No Data')
                    try:
                        pubdate_month_list.append(
                            paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Month'])
                    except KeyError:
                        pubdate_month_list.append('No Data')

                    authors = paper['MedlineCitation']['Article']['AuthorList']
                    author_names = []
                    author_affiliations = []
                    for author in authors:
                        if 'LastName' in author:
                            full_name = author['LastName']
                            if 'ForeName' in author:
                                full_name += ' ' + author['ForeName']
                            author_names.append(full_name)
                        if 'AffiliationInfo' in author and author['AffiliationInfo']:
                            author_affiliations.append(author['AffiliationInfo'][0]['Affiliation'])
                        else:
                            author_affiliations.append('No Affiliation')

                    author_list.append(', '.join(author_names))
                    affiliation_list.append('; '.join(author_affiliations))

                    pubmed_id = paper['MedlineCitation']['PMID']
                    link = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
                    link_list.append(link)

                    pubmed_id = paper['MedlineCitation']['PMID']
                    pubmedID.append(pubmed_id)

                    try:
                        keywords = paper['MedlineCitation']['KeywordList']
                        if keywords:
                            keyword_list.append(', '.join([keyword.strip() for keyword in keywords[0]]))
                        else:
                            keyword_list.append('No Keywords')
                    except KeyError:
                        keyword_list.append('No Keywords')

                    try:
                        funding_info = paper['MedlineCitation']['Article'].get('GrantList', [])
                        if funding_info:
                            grants = []
                            for grant in funding_info:
                                grant_id = grant.get('GrantID', 'Unknown GrantID')
                                agency = grant.get('Agency', 'Unknown Agency')
                                grants.append(f"{grant_id} ({agency})")
                            funding_list.append('; '.join(grants))
                        else:
                            funding_list.append('No Funding Information')
                    except KeyError:
                        funding_list.append('No Funding Information')

                    try:
                        mesh_headings = paper['MedlineCitation']['MeshHeadingList']
                        mesh_descriptor_names = []
                        for mesh in mesh_headings:
                            descriptor_name = mesh['DescriptorName'].strip()
                            mesh_descriptor_names.append(descriptor_name)
                        mesh_list.append('; '.join(mesh_descriptor_names))
                    except KeyError:
                        mesh_list.append('No Mesh Headings')

                df = pd.DataFrame({
                    'Title': title_list,
                    'PMID': pubmedID,
                    'Abstract': abstract_list,
                    'Journal': journal_list,
                    'Language': language_list,
                    'Year': pubdate_year_list,
                    'Month': pubdate_month_list,
                    'Authors': author_list,
                    'Affiliations': affiliation_list,
                    'Funding_Information': funding_list,
                    'Mesh_Headings': mesh_list,
                    'Link': link_list,
                    'Keywords': keyword_list
                })

                month_mapping = {
                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
                    'No Data': np.nan
                }
                df['Month'] = df['Month'].replace(month_mapping)

                st.write(df)
                st.download_button(
                    label="Download CSV",
                    data=df.to_csv(index=False).encode(),
                    file_name="pubmed_papers.csv",
                    mime="text/csv"
                )

                formatted_text = ""
                for i, row in df.iterrows():
                    formatted_text += f"Title: {row['Title']}\n"
                    formatted_text += f"PMID: {row['PMID']}\n"
                    formatted_text += f"Abstract: {row['Abstract']}\n"
                    formatted_text += f"Journal: {row['Journal']}\n"
                    formatted_text += f"Language: {row['Language']}\n"
                    formatted_text += f"Year: {row['Year']}\n"
                    formatted_text += f"Month: {row['Month']}\n"
                    formatted_text += f"Authors: {row['Authors']}\n"
                    formatted_text += f"Affiliations: {row['Affiliations']}\n"
                    formatted_text += f"Funding Information: {row['Funding_Information']}\n"
                    formatted_text += f"Mesh Headings: {row['Mesh_Headings']}\n"
                    formatted_text += f"Link: {row['Link']}\n"
                    formatted_text += f"Keywords: {row['Keywords']}\n\n"

                st.download_button(
                    label="Download Formatted TXT",
                    data=formatted_text.encode(),
                    file_name="pubmed_papers_formatted.txt",
                    mime="text/plain"
                )