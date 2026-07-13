# 📧 Cold Email Generator using LangChain, Groq LLM, and Streamlit

This project automates the generation of personalized **cold emails** for job opportunities found on career pages.  
It uses **LangChain**, **Groq’s Llama 3-70B model**, and **Streamlit** to:
- Scrape job postings from a given URL
- Extract key job details (role, skills, experience, description)
- Match the job skills with your **portfolio links**
- Generate a professional cold email pitch on behalf of **AtliQ**

---

## 🚀 Features
- **Web scraping** of job descriptions via `WebBaseLoader`
- **Job data extraction** with LLM and JSON parsing
- **Portfolio matching** using ChromaDB vector search
- **Cold email generation** tailored to the job posting
- **Streamlit interface** for quick and easy usage

---

## 🛠 Tech Stack
- **Python 3.10+**
- **LangChain**
- **Groq API (Llama3-70B-8192)**
- **Streamlit**
- **ChromaDB**
- **Pandas**
- **dotenv** for environment variables

---

## 📋 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/cold-email-generator.git
cd cold-email-generator
```
---

###  Run the Streamlit App
```bash
streamlit run app/streamlit_app.py
```

---

### Deploy
LINK:-https://cold-email-generator-lvu9.onrender.com

---
### Screenshot
<img width="2370" height="1273" alt="image" src="https://github.com/user-attachments/assets/8cc8916f-a068-4500-819d-6c26a421b141" />
<img width="2328" height="1110" alt="image" src="https://github.com/user-attachments/assets/63cbcf8c-35a5-40ef-9a55-a5a2b1019bca" />

