# bluepod
##### Meet Blue, the Wise Sauropod: Your Smart, Tech-Savvy Assistant 
###### powered by LangChain 🦜🔗 and GPT-4 🚀

Step into the future with Blue, a delightful blend of prehistoric wisdom and modern technology. Once a simple sauropod enjoying the prehistoric wilderness, Blue has evolved into a sophisticated digital assistant, adept at navigating the vast terrains of information in the digital age. 

Please note you should get an OpenAI API key : https://platform.openai.com/

#### Capabilities and Features:
1. PaperMiner for Scientific Exploration: Harness Blue's ability to fetch and organize academic resources. With just a keyword          or title, Blue can retrieve the latest scientific papers from PubMed, organize them neatly, and even prepare them for                download, making research seamless and efficient.

2. RAG (Retrieval-Augmented Generation) with a Twist: Utilizing the advanced capabilities of ChatGPT, Blue can generate comprehensive README files for specific PubMed IDs, transforming complex information into easy-to-digest summaries.

3. DinoDrafts for Career Development: Through the power of Natural Language Processing (NLP), Blue provides insightful analyses of resumes, crafts personalized cover letters, and offers career advice tailored to your specific needs, helping you navigate your career path with confidence.

4. Text Talk: PDF Edition: Interact with your PDFs on a whole new level. Ask Blue questions in natural language, and get precise answers pulled directly from your documents, using Conversational AI.

5. YouTube: Beyond the Play Button: Discover the potential of dynamic prompt generation with GPT-4 for tasks such as video summarization, sentiment analysis, and content recommendations, ensuring that every interaction is as informative and relevant as possible.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Before you begin installing these libraries, ensure you have Python installed on your system. It’s also good practice to use a virtual environment for Python projects to manage dependencies without conflicts. 

Here’s a quick guide on setting up a virtual environment for this project to manage these dependencies effectively:
```
pip install virtualenv
virtualenv myenv
source myenv/bin/activate  # On Unix or MacOS
myenv\Scripts\activate  # On Windows
```
### Installing 
```
pip install streamlit python-dotenv PyPDF2 biopython langchain langchain_openai langchain_community faiss-cpu python-docx requests beautifulsoup4 markdownify youtube-transcript-api
```
For example : 
```
pip install langchain
```
<img width="566" alt="Screenshot 2024-04-17 at 8 25 45 PM" src="https://github.com/melanieloaiza/bluepod/assets/72766590/d8b82e02-744b-48cf-898d-d2ca69702fcf">

### Deployment
Python 3.11.5 

Install all required packages using: 
```
pip install -r requirements.txt
```
Run app.py 
```
streamlit run app.py
```

### Built With
- [Streamlit](https://streamlit.io) -  A framework for rapidly developing and deploying interactive web applications that handle data retrieval and user interactions. 
- [Langchain](https://www.langchain.com) -  A framework for integrating advanced NLP capabilities, utilizing large language models for tasks like conversational AI and text summarization.
- [ChatGPT-4](https://openai.com/gpt-4)  -  An advanced language model designed for generating human-like text, suitable for various applications including chatbots and content generation.

### Authors
Melanie R Loaiza 

### License
This project is licensed under the MIT License - see the LICENSE.md file for details
