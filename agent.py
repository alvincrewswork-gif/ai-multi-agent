import os
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

# ============================================
# SETUP - Load keys from .env file
# ============================================
load_dotenv()

claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
chatgpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================
# CLAUDE - With built-in web search
# ============================================
def ask_claude(prompt):
    print("\n🔍 Claude is searching and thinking...")

    response = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search"
        }],
        messages=[{"role": "user", "content": prompt}]
    )

    result = ""
    for block in response.content:
        if hasattr(block, 'text'):
            result += block.text

    return result if result else "No response generated."

# ============================================
# CHATGPT - Reviews Claude's answer
# ============================================
def ask_chatgpt(prompt):
    print("\n🤖 ChatGPT is reviewing...")

    response = chatgpt.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ============================================
# MULTI-AGENT PIPELINE
# ============================================
def multi_agent(user_input):
    print("\n" + "="*50)
    print(f"YOUR QUESTION: {user_input}")
    print("="*50)

    claude_response = ask_claude(user_input)
    print(f"\n📘 CLAUDE SAYS:\n{claude_response}")

    review_prompt = (
        f"The user asked: {user_input}\n\n"
        f"Claude answered using live web search:\n{claude_response}\n\n"
        f"Please review Claude's response. Add anything important "
        f"that is missing, offer a different perspective if you have "
        f"one, or confirm and expand if you agree. Be concise and helpful."
    )

    chatgpt_response = ask_chatgpt(review_prompt)
    print(f"\n📗 CHATGPT ADDS:\n{chatgpt_response}")
    print("\n" + "="*50)

# ============================================
# RUN THE AGENT
# ============================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 Multi-Agent AI System")
    print("⚡ Powered by Claude + ChatGPT + Web Search")
    print("="*50)
    print("Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("Ask your agents anything: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "quit":
                print("\n👋 Goodbye!")
                break
            multi_agent(user_input)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")