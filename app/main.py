import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader

def create_streamlit_app(chain, portfolio, clean_text):
    st.title("Cold Mail Generator")

    # Input URL
    url_input = st.text_input("Enter a Job URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load content from the URL
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            # Load and process portfolio
            portfolio.load_portfolio()

            # Extract job listings from cleaned data
            jobs = chain.extract_jobs(data)

            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)

                # Generate cold mail
                email = chain.write_mail(job, links)

                # Display the generated email
                st.subheader(f"Email for: {job.get('role', 'Unknown Role')}")
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()

    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    
    create_streamlit_app(chain, portfolio, clean_text)
