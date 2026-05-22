# AI Multi-Agent System

A Python-based multi-agent AI system that combines Claude and ChatGPT 
to collaborate on answering questions with live web search capability.

## What it does
- Uses Claude (Anthropic) to search the web and generate answers
- Uses ChatGPT (OpenAI) to review and add perspective
- Two AIs collaborating in real time on every question

## Tech Stack
- Python 3.13
- Anthropic API (Claude Sonnet 4.6)
- OpenAI API (GPT-4o-mini)
- Live web search via Claude's built-in search tool

## Setup
1. Clone this repo
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Add your API keys to a `.env` file
5. Run: `python agent.py`# ai-multi-agent
