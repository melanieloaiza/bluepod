# bluePod 🦕
##### Meet Blue, the Wise Sauropod: Your Smart, Tech-Savvy Assistant 
###### powered by LangChain 🦜🔗 and GPT-4 🚀

Step into the future with bluePod, a delightful blend of prehistoric wisdom and modern technology. Once a simple sauropod enjoying the prehistoric wilderness, bluePod has evolved into a sophisticated digital assistant, adept at navigating the vast terrains of information in the digital age. 

### Capabilities and Features:
1. PaperMiner for Scientific Exploration: Harness Blue's ability to fetch and organize academic resources. With just a keyword          or title, Blue can retrieve the latest scientific papers from PubMed, organize them neatly, and even prepare them for                download, making research seamless and efficient. Utilizing the advanced capabilities of ChatGPT, Blue can generate comprehensive    README files for specific PubMed IDs, transforming complex information into easy-to-digest summaries.

2. DinoDrafts for Career Development: Through the power of Natural Language Processing (NLP), Blue provides insightful analyses of resumes, crafts personalized cover letters, and offers career advice tailored to your specific needs, helping you navigate your career path with confidence.

3. Text Talk: PDF Edition: Interact with your PDFs on a whole new level. Ask Blue questions in natural language, and get precise answers pulled directly from your documents, using Conversational AI.

4. YouTube: Beyond the Play Button: Discover the potential of dynamic prompt generation with GPT-4 for tasks such as video summarization, sentiment analysis, and content recommendations, ensuring that every interaction is as informative and relevant as possible.

   ##### Please refer to the documentation details provided in the main directory for descriptions of the functions used and their respective features (e.g., readmefile - documentation). 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. 
 1. Get an OpenAI API key : https://platform.openai.com/
 2. Set up the coding environment
 3. Build the app - Streamlit
 4. Deploy the app 

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

### Try it! 
Here is what it should look like: 

<img width="500" alt="image1" src="https://github.com/melanieloaiza/bluepod/assets/72766590/a63360b2-81a8-42eb-a060-15ecd2756ba5">


PaperMiner:  

<img width="500" alt="paperminer" src="https://github.com/melanieloaiza/bluepod/assets/72766590/3fd7ee18-e77c-4ca4-a829-0875d1aed1a7">


CareerPath Insights:  

<img width="500" alt="careerPath" src="https://github.com/melanieloaiza/bluepod/assets/72766590/5e2a8909-9127-43ff-9b25-af0f976a2374">


Chatbot: 

<img width="500" alt="chatbot" src="https://github.com/melanieloaiza/bluepod/assets/72766590/da27636b-7674-4efd-bac2-6002effe30e2">


Videos:

<img width="500" alt="videos" src="https://github.com/melanieloaiza/bluepod/assets/72766590/79c9f233-20c6-4f7e-be58-c2fd8b2db67f">

### Built With
- [Streamlit](https://streamlit.io) -  A framework for rapidly developing and deploying interactive web applications that handle data retrieval and user interactions. 
- [Langchain](https://www.langchain.com) -  A framework for integrating advanced NLP capabilities, utilizing large language models for tasks like conversational AI and text summarization.
- [ChatGPT-4](https://openai.com/gpt-4)  -  An advanced language model designed for generating human-like text, suitable for various applications including chatbots and content generation.

### Author
Melanie R Loaiza 

### License
This project is licensed under the MIT License - see the LICENSE.md file for details
