import streamlit as st
from st_pages import Page, show_pages, add_page_title
from style import css

def main():
    st.set_page_config(
        page_title="bluepod",
        page_icon=" "
    )
    show_pages(
        [
            Page("app.py", "Home Page"),
            Page("pages/README file.py", "PaperMiner", "*"),
            Page("pages/resume.py", "CareerPath Insights", "*"),
            Page("pages/chatbot.py", "Chatbot", "*"),
            Page("pages/videos.py", "Videos", "*")
        ]
    )
    # Start Top Information
    st.markdown('<span style="font-size: 100px;">🦕</span>', unsafe_allow_html=True)
    st.markdown('<div class="gradient-text">bluePod</div>', unsafe_allow_html=True)
    st.caption("powered by LangChain 🦜🔗 and GPT-4 🚀")
    st.markdown(css, unsafe_allow_html=True)

    st.markdown(
        "Hey there! I'm Blue, the wise sauropod. Back in my day, munching on lush, leafy greens was the highlight. But times have evolved, and so have I. Now, I thrive on digesting information from PDFs, Websites, and YouTube Videos—keeping pace with my tech-savvy herbivore peers. \n\n"
        " Here's a peek at the cool abilities I've developed for you: \n\n  "
    )

    st.markdown('<div class="gradient-subtitle"> PaperMiner for Scientific Purposes </div>', unsafe_allow_html=True)
    st.markdown(
        "* **Web Mining** :  I can fetch a list of 5 recent academic papers from PubMed based on your keyword or title, neatly organize them into a data frame, and offer the compiled data for download as a text file. Perfect for staying on top of your field! \n\n "
        "* **RAG (Retrieval-Augmented Generation) with a Twist** : Using ChatGPT's prowess, I can craft a README file from any PubMed ID you're curious about. It's about making information easy to digest and ready to share. "
    )

    st.markdown('<div class="gradient-subtitle"> DinoDrafts: Navigating Your Career Path </div>', unsafe_allow_html=True)
    st.markdown(
        "* Through the lens of **NLP (Natural Language Processing)**, I analyze resumes, offer constructive feedback, and craft cover letters tailored to specific job positions. It's your career journey, but with a touch of analytical precision.  "
    )

    st.markdown('<div class="gradient-subtitle"> Text Talk: PDF Edition </div>', unsafe_allow_html=True)
    st.markdown(
        "* Dive into PDFs interactively. Ask me natural language questions, and I'll fetch the answers using **Conversational AI**. It's like having a chat with your documents!"
    )

    st.markdown('<div class="gradient-subtitle"> Youtube: Beyond the Play Button </div>', unsafe_allow_html=True)
    st.markdown(
        "* **Prompt-based Generation** : Experience dynamic prompt generation with OpenAI's GPT-4 for tasks like summarization, sentiment analysis, or finding similar content. With a knack for contextual understanding, I ensure the summaries and recommendations are as relevant and informative as your needs."
    )

    with st.sidebar:
        linkedin_url = "https://www.linkedin.com/in/melanieloaiza/"
        st.markdown("**bluePod - V0.1** "
            , unsafe_allow_html=True
        )
        st.markdown(
            '<div class="text-justify">Drawing inspiration from sauropods, aims to enhance interaction by embodying their remarkable traits. '
            'Like the sauropods adaptability seen in fossils across continents, bluePod leverages advanced technologies such '
            'as LangChain and OpenAI\'s GPT-4. Through this, it enhances human-machine interaction, fostering adaptability in a rapidly evolving digital world.'
            '</div>', unsafe_allow_html=True
        )

        st.markdown(
            '**Contact information:** <a href="https://www.linkedin.com/in/melanieloaiza/" target="_blank">Melanie R Loaiza</a>',
            unsafe_allow_html=True)


if __name__ == "__main__":
    main()
