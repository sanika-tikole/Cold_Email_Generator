import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()  # Load environment variables from .env file


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("API_KEY"),  # Use environment variable for safety
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:

            {page_data}

            ### INSTRUCTION:

            The scraped text is from the career's page of a website.

            Your job is to extract only the single most relevant job posting and return it in JSON format containing the following keys: 'role', 'experience', 'skills' and 'description'.

            Only return one valid JSON object in dict format.

            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm

        res = chain_extract.invoke({"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big, unable to parse jobs")
        return res

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:

            You are Alex, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company focused on the seamless integration of business processes through automated tools.

            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering process optimization, cost reduction, and heightened overall efficiency.

            Your job is to write a cold email to the client regarding the job mentioned above and pitch how AtliQ can assist in fulfilling their needs.

            Use the actual role, skills, and description from the job posting as the source of truth.
            Keep the email aligned with that role and do not invent a different job title or skill set.

            Also add the most relevant ones from the following links to showcase AtliQ's portfolio.

            Remember you are Alex, BDE at AtliQ.

            Do not provide a preamble.

            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm

        res = chain_email.invoke({
            "job_description": str(job),
            "link_list": links
        })

        return res.content


if __name__ == "__main__":
    print("Loaded API key:", os.getenv('API_KEY'))
