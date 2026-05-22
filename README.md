# 🤖 AI Multi-Agent Platform

A full-featured AI platform built with Python and Streamlit that combines 
**Claude (Anthropic)** and **ChatGPT (OpenAI)** to collaborate on 22 different tools 
across 5 categories — with live web search built in.

Built by [@alvincrewswork-gif](https://github.com/alvincrewswork-gif)

---

## 🚀 What It Does

Instead of using one AI, this platform uses **two AIs working together** — 
Claude answers first (with live web search), then ChatGPT reviews and adds 
its perspective. Or flip it — you choose who goes first.

---

## 🗂️ Features (22 Total)

### 💬 Chat
- **Multi-Agent Chat** — Ask anything and get two AI perspectives with live web search

### 🛠️ AI Tools
- **URL Summarizer** — Paste any link and get an instant summary
- **Document Q&A** — Upload a file and ask questions about it
- **Translator** — Translate to 15 languages with tone control
- **Code Assistant** — Explain, debug, write, or optimize code
- **Meeting Notes** — Turn messy notes into clean summaries and action items
- **Research Assistant** — Deep dive any topic with both AIs simultaneously

### 🎨 Creative
- **Writing Assistant** — Blog posts, emails, social captions and more
- **AI Debate** — Watch Claude and ChatGPT argue both sides of any topic
- **Idea Generator** — Brainstorm business, app, and content ideas
- **Quiz Generator** — Generate quizzes on any topic with answer keys
- **Content Repurposer** — Turn one piece of content into multiple formats

### 💼 Career
- **Project Tracker** — Log and track your portfolio projects
- **Resume Generator** — Turn projects into ATS-friendly resume bullets
- **Job Analyzer** — Paste a job posting and get tailored advice
- **Interview Coach** — Practice questions for any role
- **LinkedIn Bio Generator** — Write a compelling profile summary
- **Cold Email Writer** — Write cold emails that get responses
- **Salary Negotiation Coach** — Scripts and strategies to negotiate pay

### 👨‍💻 Developer
- **Learning Roadmap** — Personalized study plans for any tech skill
- **Error Explainer** — Paste any error and get a plain English fix
- **Code Documenter** — Auto-generate comments and documentation
- **Prompt Engineer** — Improve your AI prompts for better results
- **App Idea Validator** — Get honest market feedback on your app idea

---

## 🛠️ Tech Stack

- **Python 3.13**
- **Streamlit** — Web interface
- **Anthropic API** — Claude Sonnet 4.6 with built-in web search
- **OpenAI API** — GPT-4o-mini
- **BeautifulSoup4** — Web scraping for URL summarizer
- **GitHub** — Version control

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/alvincrewswork-gif/ai-multi-agent.git
cd ai-multi-agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API keys
Create a `.env` file in the root folder: