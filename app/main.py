import streamlit as st
import streamlit.components.v1 as components
import requests
import html
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
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(180deg, #f7fbff 0%, #eef4ff 100%);
            }

            .hero-card {
                background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #38bdf8 100%);
                color: white;
                padding: 1.4rem 1.6rem;
                border-radius: 18px;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.18);
                margin-bottom: 1rem;
            }

            .hero-card h1 {
                margin: 0;
                font-size: 2rem;
            }

            .hero-card p {
                margin: 0.35rem 0 0;
                opacity: 0.92;
            }

            div.stButton > button {
                background: linear-gradient(90deg, #1d4ed8, #0ea5e9);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.6rem 1.25rem;
                font-weight: 600;
                box-shadow: 0 10px 20px rgba(29, 78, 216, 0.2);
                transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
            }

            div.stButton > button:hover {
                background: linear-gradient(90deg, #1e40af, #0284c7);
                color: white;
                border: none;
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 14px 28px rgba(29, 78, 216, 0.28);
            }

            div[data-baseweb="input"] {
                background: white !important;
                border: 2px solid #2563eb !important;
                border-radius: 12px !important;
                box-shadow: 0 8px 20px rgba(37, 99, 235, 0.12);
                transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
            }

            div[data-baseweb="input"] input {
                background: white !important;
                color: #0f172a !important;
            }

            div[data-baseweb="input"]:hover {
                box-shadow: 0 12px 26px rgba(37, 99, 235, 0.18);
                transform: translateY(-1px);
            }

            div[data-baseweb="input"]:focus-within {
                border-color: #1d4ed8 !important;
                box-shadow: 0 14px 30px rgba(29, 78, 216, 0.22);
            }

            div[data-baseweb="input"] input::placeholder {
                color: #64748b !important;
            }

            .stTextInput label {
                color: #0f172a !important;
                font-weight: 600;
            }

            div[data-testid="stCodeBlock"] {
                background: #f8fbff !important;
                border: 1px solid #cfe0ff !important;
                border-radius: 16px !important;
                box-shadow: 0 12px 28px rgba(37, 99, 235, 0.10);
            }

            div[data-testid="stCodeBlock"] pre {
                background: #f8fbff !important;
                color: #0f172a !important;
            }

            .email-card {
                background: #f8fbff;
                border: 1px solid #cfe0ff;
                border-radius: 16px;
                box-shadow: 0 12px 28px rgba(37, 99, 235, 0.10);
                padding: 1rem 1.1rem;
                color: #0f172a;
                white-space: pre-wrap;
                line-height: 1.65;
                font-size: 0.98rem;
            }

            .email-card-header {
                margin-bottom: 0.6rem;
                font-weight: 700;
                color: #1d4ed8;
                font-size: 1rem;
            }
        </style>
        <div class="hero-card">
            <h1>Cold Mail Generator</h1>
            <p>Paste a job URL and generate a tailored outreach email in one click.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
            escaped_email = html.escape(email)
            components.html(
                f"""
                <div style="position: relative; background: #f8fbff; border: 1px solid #cfe0ff; border-radius: 16px; box-shadow: 0 12px 28px rgba(37, 99, 235, 0.10); padding: 1rem 1.1rem; color: #0f172a;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                        <div style="font-weight: 700; color: #1d4ed8; font-size: 1rem;">Generated Email</div>
                        <button id="copyBtn" style="background: linear-gradient(90deg, #1d4ed8, #0ea5e9); color: white; border: none; border-radius: 10px; padding: 0.45rem 0.8rem; font-weight: 600; cursor: pointer; box-shadow: 0 8px 18px rgba(29, 78, 216, 0.20);">Copy</button>
                    </div>
                    <pre id="emailText" style="margin: 0; white-space: pre-wrap; line-height: 1.65; font-size: 0.98rem; color: #0f172a; font-family: inherit; overflow-x: auto;">{escaped_email}</pre>
                </div>
                <script>
                    const button = document.getElementById('copyBtn');
                    const emailText = document.getElementById('emailText');

                    button.addEventListener('click', async () => {{
                        try {{
                            await navigator.clipboard.writeText(emailText.innerText);
                            const original = button.innerText;
                            button.innerText = 'Copied';
                            setTimeout(() => {{ button.innerText = original; }}, 1500);
                        }} catch (error) {{
                            button.innerText = 'Copy failed';
                        }}
                    }});
                </script>
                """,
                height=600,
                scrolling=True,
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()

    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    
    create_streamlit_app(chain, portfolio, clean_text)
