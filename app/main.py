import streamlit as st
import requests
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def load_page_text(url):
    response = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    text = clean_text(response.text)

    if "404 this page could not be found" in text.lower():
        raise ValueError("The page returned a generic 404 shell instead of the actual job description.")

    return text

def create_streamlit_app(chain, portfolio, clean_text):
    st.title("Cold Mail Generator")

    # Input URL
    url_input = st.text_input("Enter a Job URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load content from the URL
            data = load_page_text(url_input)

            # Load and process portfolio
            portfolio.load_portfolio()

            # Extract job listings from cleaned data
            job = chain.extract_jobs(data)
            if isinstance(job, list):
                job = job[0] if job else {}

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
