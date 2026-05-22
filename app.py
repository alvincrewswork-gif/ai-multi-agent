import os
import json
import requests
import streamlit as st
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
chatgpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="AI Multi-Agent Platform",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# AI FUNCTIONS
# ============================================
def ask_claude(prompt):
    response = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )
    result = ""
    for block in response.content:
        if hasattr(block, 'text'):
            result += block.text
    return result if result else "No response generated."

def ask_chatgpt(prompt):
    response = chatgpt.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ============================================
# PROJECT TRACKER HELPERS
# ============================================
PROJECTS_FILE = "projects.json"

def load_projects():
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_projects(projects):
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=2)

# ============================================
# NAVIGATION
# ============================================
if "page" not in st.session_state:
    st.session_state.page = "💬 Multi-Agent Chat"

def nav(label):
    if st.sidebar.button(label, use_container_width=True):
        st.session_state.page = label
        st.rerun()

st.sidebar.title("🤖 AI Platform")
st.sidebar.markdown("---")

st.sidebar.markdown("### 💬 CHAT")
nav("💬 Multi-Agent Chat")

st.sidebar.markdown("### 🛠️ AI TOOLS")
nav("🔗 URL Summarizer")
nav("📄 Document Q&A")
nav("🌐 Translator")
nav("💻 Code Assistant")
nav("📝 Meeting Notes")
nav("🌍 Research Assistant")

st.sidebar.markdown("### 🎨 CREATIVE")
nav("✍️ Writing Assistant")
nav("🎭 AI Debate")
nav("💡 Idea Generator")
nav("🧠 Quiz Generator")
nav("🔄 Content Repurposer")

st.sidebar.markdown("### 💼 CAREER")
nav("📋 Project Tracker")
nav("📄 Resume Generator")
nav("🎯 Job Analyzer")
nav("🎤 Interview Coach")
nav("🔗 LinkedIn Bio")
nav("📧 Cold Email Writer")
nav("💰 Salary Negotiation Coach")

st.sidebar.markdown("### 👨‍💻 DEVELOPER")
nav("📚 Learning Roadmap")
nav("🐛 Error Explainer")
nav("📖 Code Documenter")
nav("🎨 Prompt Engineer")
nav("📱 App Idea Validator")

st.sidebar.markdown("---")
st.sidebar.caption("Built by alvincrewswork-gif")

page = st.session_state.page

# ============================================
# PAGE: MULTI-AGENT CHAT
# ============================================
if page == "💬 Multi-Agent Chat":
    st.title("💬 Multi-Agent Chat")
    st.subheader("Two AIs collaborating with live web search")

    ai_first = st.radio(
        "🎮 Choose which AI goes first:",
        ["Claude first, ChatGPT reviews", "ChatGPT first, Claude reviews"],
        horizontal=True
    )
    st.divider()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask your agents anything..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        if "Claude first" in ai_first:
            with st.chat_message("assistant", avatar="📘"):
                with st.spinner("🔍 Claude is searching and thinking..."):
                    first_response = ask_claude(prompt)
                st.markdown("**📘 Claude says:**")
                st.markdown(first_response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"**📘 Claude says:**\n\n{first_response}"
            })
            with st.chat_message("assistant", avatar="📗"):
                with st.spinner("🤖 ChatGPT is reviewing..."):
                    review = ask_chatgpt(
                        f"User asked: {prompt}\n\n"
                        f"Claude answered: {first_response}\n\n"
                        f"Review and add your perspective. Be concise."
                    )
                st.markdown("**📗 ChatGPT adds:**")
                st.markdown(review)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"**📗 ChatGPT adds:**\n\n{review}"
            })
        else:
            with st.chat_message("assistant", avatar="📗"):
                with st.spinner("🤖 ChatGPT is thinking..."):
                    first_response = ask_chatgpt(prompt)
                st.markdown("**📗 ChatGPT says:**")
                st.markdown(first_response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"**📗 ChatGPT says:**\n\n{first_response}"
            })
            with st.chat_message("assistant", avatar="📘"):
                with st.spinner("🔍 Claude is searching and reviewing..."):
                    review = ask_claude(
                        f"User asked: {prompt}\n\n"
                        f"ChatGPT answered: {first_response}\n\n"
                        f"Review, search web if needed, add your perspective."
                    )
                st.markdown("**📘 Claude adds:**")
                st.markdown(review)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"**📘 Claude adds:**\n\n{review}"
            })

# ============================================
# PAGE: URL SUMMARIZER
# ============================================
elif page == "🔗 URL Summarizer":
    st.title("🔗 URL Summarizer")
    st.subheader("Paste any URL and get an instant summary")

    url = st.text_input("Paste a URL", placeholder="https://example.com/article")
    summary_style = st.selectbox("Summary style", [
        "Brief overview (3-5 sentences)",
        "Detailed summary with key points",
        "Bullet points only",
        "ELI5 (Explain like I'm 5)"
    ])

    if st.button("📝 Summarize", type="primary"):
        if url:
            with st.spinner("Fetching and summarizing..."):
                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    r = requests.get(url, headers=headers, timeout=10)
                    soup = BeautifulSoup(r.content, "html.parser")
                    for tag in soup(["script", "style", "nav", "footer"]):
                        tag.decompose()
                    text = soup.get_text(separator=" ", strip=True)[:5000]
                    summary = ask_claude(
                        f"Summarize this webpage in this style: {summary_style}\n\n"
                        f"URL: {url}\n\nContent: {text}"
                    )
                    st.markdown("### 📝 Summary:")
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"Could not fetch URL: {e}")

# ============================================
# PAGE: DOCUMENT Q&A
# ============================================
elif page == "📄 Document Q&A":
    st.title("📄 Document Q&A")
    st.subheader("Upload a document and ask questions about it")

    uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "py", "md"])
    question = st.text_input("What do you want to know about this document?")

    if st.button("🔍 Ask", type="primary"):
        if uploaded_file and question:
            with st.spinner("Reading and thinking..."):
                if uploaded_file.type == "application/pdf":
                    try:
                        import PyPDF2
                        reader = PyPDF2.PdfReader(uploaded_file)
                        content = ""
                        for pg in reader.pages:
                            content += pg.extract_text()
                    except Exception:
                        st.error("PDF error. Try a .txt file.")
                        content = ""
                else:
                    content = uploaded_file.read().decode("utf-8", errors="ignore")
                if content:
                    answer = ask_claude(
                        f"Document:\n\n{content[:6000]}\n\n"
                        f"Question: {question}\n\nAnswer based on the document."
                    )
                    st.markdown("### 💬 Answer:")
                    st.markdown(answer)

# ============================================
# PAGE: TRANSLATOR
# ============================================
elif page == "🌐 Translator":
    st.title("🌐 Translator")
    st.subheader("Translate anything to any language")

    col1, col2 = st.columns(2)
    with col1:
        source_text = st.text_area("Text to translate", height=200)
    with col2:
        target_language = st.selectbox("Translate to", [
            "Spanish", "French", "German", "Italian", "Portuguese",
            "Japanese", "Chinese (Simplified)", "Korean", "Arabic",
            "Russian", "Hindi", "Dutch", "Swedish", "Greek", "Polish"
        ])
        tone = st.selectbox("Tone", ["Formal", "Casual", "Business"])

    if st.button("🌐 Translate", type="primary"):
        if source_text:
            with st.spinner(f"Translating to {target_language}..."):
                translation = ask_claude(
                    f"Translate to {target_language} in a {tone.lower()} tone.\n\n"
                    f"Text: {source_text}\n\nProvide only the translation."
                )
            st.markdown(f"### 🌐 {target_language} Translation:")
            st.markdown(translation)

# ============================================
# PAGE: CODE ASSISTANT
# ============================================
elif page == "💻 Code Assistant":
    st.title("💻 Code Assistant")
    st.subheader("Explain, debug, or write code with both AIs")

    action = st.radio("What do you need?", [
        "Explain this code", "Debug this code",
        "Write code for me", "Optimize this code"
    ], horizontal=True)

    code_input = st.text_area(
        "Describe what you want" if action == "Write code for me" else "Paste your code here",
        height=250
    )
    language = st.selectbox("Language", ["Python", "JavaScript", "HTML/CSS", "SQL", "Bash"])

    if st.button("💻 Go", type="primary"):
        if code_input:
            with st.spinner("Both AIs working on your code..."):
                claude_response = ask_claude(
                    f"Task: {action}\nLanguage: {language}\n\n"
                    f"Code/Request:\n{code_input}\n\nBe clear and practical."
                )
                chatgpt_response = ask_chatgpt(
                    f"Task: {action} in {language}\n\n"
                    f"Code/Request:\n{code_input}\n\n"
                    f"Claude said:\n{claude_response}\n\n"
                    f"Add anything missing or a different approach."
                )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📘 Claude:")
                st.markdown(claude_response)
            with col2:
                st.markdown("### 📗 ChatGPT:")
                st.markdown(chatgpt_response)

# ============================================
# PAGE: MEETING NOTES
# ============================================
elif page == "📝 Meeting Notes":
    st.title("📝 Meeting Notes")
    st.subheader("Turn messy notes into clean summaries and action items")

    raw_notes = st.text_area("Paste your raw meeting notes", height=250,
        placeholder="Paste messy notes, transcript, or bullet points...")

    col1, col2 = st.columns(2)
    with col1:
        meeting_type = st.selectbox("Meeting type", [
            "Team standup", "Project planning", "Client meeting",
            "Brainstorm session", "Performance review", "General meeting"
        ])
    with col2:
        output_style = st.selectbox("Output style", [
            "Executive summary + action items",
            "Detailed notes with sections",
            "Action items only",
            "Email summary to send to attendees"
        ])

    if st.button("📝 Clean Up Notes", type="primary"):
        if raw_notes:
            with st.spinner("Organizing your meeting notes..."):
                clean_notes = ask_claude(
                    f"Clean up these {meeting_type} notes into: {output_style}\n\n"
                    f"Raw notes:\n{raw_notes}\n\n"
                    f"Format clearly with key decisions, action items, "
                    f"discussion points and next steps."
                )
            st.markdown("### 📝 Clean Meeting Notes:")
            st.markdown(clean_notes)

# ============================================
# PAGE: RESEARCH ASSISTANT
# ============================================
elif page == "🌍 Research Assistant":
    st.title("🌍 Research Assistant")
    st.subheader("Deep dive any topic with both AIs searching simultaneously")

    topic = st.text_input("What do you want to research?",
        placeholder="e.g. Latest developments in AI agents...")
    research_depth = st.selectbox("Research depth", [
        "Quick overview", "Detailed analysis", "Comprehensive deep dive"
    ])
    focus_areas = st.multiselect("Focus areas (optional)", [
        "Latest news and developments", "Historical background",
        "Key people and companies", "Pros and cons",
        "Future outlook", "How to get started"
    ])

    if st.button("🌍 Start Research", type="primary"):
        if topic:
            focus_text = (
                f"Focus on: {', '.join(focus_areas)}" if focus_areas
                else "Give a well-rounded overview"
            )
            col1, col2 = st.columns(2)
            with col1:
                with st.spinner("🔍 Claude is researching..."):
                    claude_research = ask_claude(
                        f"Research thoroughly: {topic}\n\n"
                        f"Depth: {research_depth}\n{focus_text}\n\n"
                        f"Search web for current info. Cite sources where possible."
                    )
                st.markdown("### 📘 Claude's Research:")
                st.markdown(claude_research)
            with col2:
                with st.spinner("🤖 ChatGPT is researching..."):
                    chatgpt_research = ask_chatgpt(
                        f"Research: {topic}\n\nDepth: {research_depth}\n\n"
                        f"Claude found:\n{claude_research}\n\n"
                        f"Add different angles Claude may have missed."
                    )
                st.markdown("### 📗 ChatGPT Adds:")
                st.markdown(chatgpt_research)

# ============================================
# PAGE: WRITING ASSISTANT
# ============================================
elif page == "✍️ Writing Assistant":
    st.title("✍️ Writing Assistant")
    st.subheader("Create any type of written content")

    content_type = st.selectbox("What are you writing?", [
        "Blog post", "Email", "Social media caption",
        "Cover letter", "Report", "Announcement", "Bio"
    ])
    topic = st.text_input("Topic or subject")
    details = st.text_area("Specific details or requirements?", height=100)
    tone = st.selectbox("Tone", ["Professional", "Casual", "Friendly", "Formal", "Persuasive"])
    length = st.selectbox("Length", ["Short", "Medium", "Long"])

    if st.button("✍️ Write It", type="primary"):
        if topic:
            with st.spinner("Writing your content..."):
                result = ask_claude(
                    f"Write a {length.lower()} {content_type.lower()} about: {topic}\n\n"
                    f"Tone: {tone}\nDetails: {details}\n\n"
                    f"Make it engaging and ready to use."
                )
            st.markdown(f"### ✍️ Your {content_type}:")
            st.markdown(result)

# ============================================
# PAGE: AI DEBATE
# ============================================
elif page == "🎭 AI Debate":
    st.title("🎭 AI Debate")
    st.subheader("Watch Claude and ChatGPT argue both sides")

    topic = st.text_input("Debate topic",
        placeholder="e.g. AI will replace most jobs in 10 years")
    claude_side = st.selectbox("Claude argues:", ["For (Pro)", "Against (Con)"])

    if st.button("🎭 Start Debate", type="primary"):
        if topic:
            chatgpt_side = "Against (Con)" if claude_side == "For (Pro)" else "For (Pro)"
            with st.spinner("Claude preparing arguments..."):
                claude_response = ask_claude(
                    f"Argue {claude_side} on: {topic}\n\n"
                    f"Give 3 strong persuasive arguments."
                )
            with st.spinner("ChatGPT preparing counter arguments..."):
                chatgpt_response = ask_chatgpt(
                    f"Argue {chatgpt_side} on: {topic}\n\n"
                    f"Claude argued {claude_side}:\n{claude_response}\n\n"
                    f"Give 3 strong counter arguments."
                )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### 📘 Claude ({claude_side}):")
                st.markdown(claude_response)
            with col2:
                st.markdown(f"### 📗 ChatGPT ({chatgpt_side}):")
                st.markdown(chatgpt_response)

# ============================================
# PAGE: IDEA GENERATOR
# ============================================
elif page == "💡 Idea Generator":
    st.title("💡 Idea Generator")
    st.subheader("Brainstorm with two AIs at once")

    idea_type = st.selectbox("What kind of ideas?", [
        "Business ideas", "App or software ideas", "Content ideas",
        "Project ideas", "Side hustle ideas", "AI project ideas"
    ])
    context = st.text_area("Tell us about yourself or your interests",
        placeholder="e.g. I'm into AI, work in education, know Python...", height=100)
    quantity = st.slider("How many ideas?", 3, 10, 5)

    if st.button("💡 Generate Ideas", type="primary"):
        if context:
            with st.spinner("Both AIs brainstorming..."):
                claude_ideas = ask_claude(
                    f"Generate {quantity} creative {idea_type} for:\n\n{context}\n\n"
                    f"Numbered list with title and 2 sentence description each."
                )
                chatgpt_ideas = ask_chatgpt(
                    f"Generate {quantity} different {idea_type} for:\n\n{context}\n\n"
                    f"Claude suggested:\n{claude_ideas}\n\n"
                    f"Come up with completely different ideas."
                )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📘 Claude's Ideas:")
                st.markdown(claude_ideas)
            with col2:
                st.markdown("### 📗 ChatGPT's Ideas:")
                st.markdown(chatgpt_ideas)

# ============================================
# PAGE: QUIZ GENERATOR
# ============================================
elif page == "🧠 Quiz Generator":
    st.title("🧠 Quiz Generator")
    st.subheader("Generate quizzes on any topic instantly")

    topic = st.text_input("Quiz topic",
        placeholder="e.g. Automotive brakes, Python basics, World War 2...")
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"])
    num_questions = st.slider("Number of questions", 5, 20, 10)
    quiz_type = st.selectbox("Question type", [
        "Multiple choice", "True or False", "Short answer", "Mixed"
    ])
    include_answers = st.checkbox("Include answer key", value=True)

    if st.button("🧠 Generate Quiz", type="primary"):
        if topic:
            with st.spinner(f"Generating {num_questions} question quiz on {topic}..."):
                prompt = (
                    f"Create a {num_questions} question {quiz_type} quiz on: {topic}\n\n"
                    f"Difficulty: {difficulty}\n\n"
                    f"Format each question clearly and number them.\n"
                    f"For multiple choice include 4 options labeled A, B, C, D.\n"
                )
                if include_answers:
                    prompt += "Include a clearly labeled answer key at the end."
                else:
                    prompt += "Do NOT include answers - teacher will use separately."
                quiz = ask_claude(prompt)
            st.markdown(f"### 🧠 {topic} Quiz:")
            st.markdown(quiz)
            if include_answers:
                st.info("Tip: Uncheck answer key to generate a student version!")

# ============================================
# PAGE: CONTENT REPURPOSER
# ============================================
elif page == "🔄 Content Repurposer":
    st.title("🔄 Content Repurposer")
    st.subheader("Turn one piece of content into many formats")

    original_content = st.text_area("Paste your original content", height=200,
        placeholder="Paste a blog post, article, email, or any text...")
    formats = st.multiselect("Repurpose into:", [
        "3 Twitter/X posts", "LinkedIn post", "Instagram caption",
        "Email newsletter", "Short summary", "5 bullet key takeaways",
        "YouTube description"
    ], default=["3 Twitter/X posts", "LinkedIn post", "Email newsletter"])
    tone = st.selectbox("Tone", ["Professional", "Casual", "Engaging", "Educational"])

    if st.button("🔄 Repurpose Content", type="primary"):
        if original_content and formats:
            with st.spinner("Repurposing your content..."):
                for fmt in formats:
                    with st.expander(f"📄 {fmt}", expanded=True):
                        result = ask_claude(
                            f"Repurpose this content into {fmt}.\n\n"
                            f"Tone: {tone}\n\nOriginal:\n{original_content}\n\n"
                            f"Make it feel native to that platform."
                        )
                        st.markdown(result)

# ============================================
# PAGE: PROJECT TRACKER
# ============================================
elif page == "📋 Project Tracker":
    st.title("📋 Project Tracker")
    st.subheader("Track your AI developer journey")

    projects = load_projects()

    with st.expander("➕ Add New Project", expanded=len(projects) == 0):
        with st.form("new_project"):
            name = st.text_input("Project Name")
            description = st.text_area("What did you build?")
            skills = st.text_input("Skills used (comma separated)")
            github = st.text_input("GitHub Link (optional)")
            completed = st.date_input("Date completed")
            submitted = st.form_submit_button("💾 Save Project")
            if submitted and name:
                projects.append({
                    "name": name, "description": description,
                    "skills": skills, "github": github, "date": str(completed)
                })
                save_projects(projects)
                st.success(f"✅ '{name}' saved!")
                st.rerun()

    st.divider()

    if not projects:
        st.info("No projects yet! Add your first one above.")
    else:
        st.markdown(f"### 🏆 {len(projects)} Project(s)")
        for i, p in enumerate(projects):
            with st.expander(f"🚀 {p['name']} — {p['date']}"):
                st.markdown(f"**Description:** {p['description']}")
                st.markdown(f"**Skills:** `{p['skills']}`")
                if p.get('github'):
                    st.markdown(f"**GitHub:** [{p['github']}]({p['github']})")
                if st.button("🗑️ Delete", key=f"del_{i}"):
                    projects.pop(i)
                    save_projects(projects)
                    st.rerun()

# ============================================
# PAGE: RESUME GENERATOR
# ============================================
elif page == "📄 Resume Generator":
    st.title("📄 Resume Bullet Generator")
    st.subheader("Turn your projects into powerful resume bullets")

    projects = load_projects()
    if projects:
        options = ["Type my own..."] + [p["name"] for p in projects]
        selected = st.selectbox("Pick a saved project or type your own:", options)
        if selected != "Type my own...":
            project = next(p for p in projects if p["name"] == selected)
            project_description = st.text_area("Project description",
                value=project["description"], height=150)
        else:
            project_description = st.text_area("Describe your project", height=150)
    else:
        project_description = st.text_area("Describe your project", height=150)

    job_target = st.text_input("What job are you targeting?")

    if st.button("✨ Generate Bullets", type="primary"):
        if project_description:
            with st.spinner("Crafting resume bullets..."):
                bullets = ask_claude(
                    f"Create 4 strong ATS-friendly resume bullets.\n\n"
                    f"Project: {project_description}\nTarget job: {job_target}\n\n"
                    f"Start with action verbs, include technologies, "
                    f"quantify impact, keep under 2 lines each."
                )
            st.markdown("### ✅ Your Resume Bullets:")
            st.markdown(bullets)

# ============================================
# PAGE: JOB ANALYZER
# ============================================
elif page == "🎯 Job Analyzer":
    st.title("🎯 Job Posting Analyzer")
    st.subheader("Paste a job posting and get tailored advice")

    col1, col2 = st.columns(2)
    with col1:
        job_posting = st.text_area("📋 Paste job posting", height=300)
    with col2:
        your_background = st.text_area("👤 Your background", height=300)

    if st.button("🎯 Analyze", type="primary"):
        if job_posting and your_background:
            with st.spinner("Analyzing..."):
                analysis = ask_claude(
                    f"Analyze this job for my background:\n\n"
                    f"JOB:\n{job_posting}\n\nMY BACKGROUND:\n{your_background}\n\n"
                    f"Provide:\n1. Skills I already have\n2. Skill gaps\n"
                    f"3. Resume tailoring tips\n4. 3 interview talking points\n"
                    f"5. Match percentage and honest assessment"
                )
            st.markdown("### 📊 Analysis:")
            st.markdown(analysis)

# ============================================
# PAGE: INTERVIEW COACH
# ============================================
elif page == "🎤 Interview Coach":
    st.title("🎤 Interview Coach")
    st.subheader("Practice interview questions for any role")

    job_role = st.text_input("Role you are interviewing for",
        placeholder="e.g. AI Developer, Data Analyst...")
    your_background = st.text_area("Your background", height=100)
    question_type = st.selectbox("Question type", [
        "General interview questions", "Technical questions",
        "Behavioral questions (STAR format)", "Questions to ask the interviewer"
    ])

    if st.button("🎤 Generate Questions + Tips", type="primary"):
        if job_role:
            with st.spinner("Preparing interview prep..."):
                claude_response = ask_claude(
                    f"Generate 5 {question_type} for {job_role}.\n\n"
                    f"Background: {your_background}\n\n"
                    f"For each: the question, why they ask it, tips for strong answer."
                )
                chatgpt_response = ask_chatgpt(
                    f"Generate 5 different {question_type} for {job_role}.\n\n"
                    f"Background: {your_background}\n\n"
                    f"Claude covered:\n{claude_response}\n\n"
                    f"Give completely different questions with tips."
                )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📘 Claude's Questions:")
                st.markdown(claude_response)
            with col2:
                st.markdown("### 📗 ChatGPT's Questions:")
                st.markdown(chatgpt_response)

# ============================================
# PAGE: LINKEDIN BIO
# ============================================
elif page == "🔗 LinkedIn Bio":
    st.title("🔗 LinkedIn Bio Generator")
    st.subheader("Write a compelling LinkedIn profile summary")

    current_role = st.text_input("Current or target job title",
        placeholder="e.g. AI Developer, IT Specialist...")
    experience = st.text_area("Your experience and background", height=100)
    skills = st.text_input("Key skills",
        placeholder="Python, AI, Claude API, Streamlit...")
    goal = st.text_input("What are you looking for?",
        placeholder="e.g. AI developer roles, freelance projects...")
    tone = st.selectbox("Tone", ["Professional", "Conversational", "Bold and confident"])

    if st.button("🔗 Generate Bio", type="primary"):
        if current_role and experience:
            with st.spinner("Writing your LinkedIn bio..."):
                bio = ask_claude(
                    f"Write a compelling LinkedIn profile summary.\n\n"
                    f"Role: {current_role}\nExperience: {experience}\n"
                    f"Skills: {skills}\nGoal: {goal}\nTone: {tone}\n\n"
                    f"Under 300 words. First person. Memorable and authentic."
                )
            st.markdown("### 🔗 Your LinkedIn Bio:")
            st.markdown(bio)

# ============================================
# PAGE: COLD EMAIL WRITER
# ============================================
elif page == "📧 Cold Email Writer":
    st.title("📧 Cold Email Writer")
    st.subheader("Write cold emails that actually get responses")

    col1, col2 = st.columns(2)
    with col1:
        recipient_role = st.text_input("Who are you emailing?",
            placeholder="e.g. Hiring Manager, CTO, Recruiter...")
        company = st.text_input("Company name")
        purpose = st.selectbox("Purpose", [
            "Job opportunity", "Freelance work",
            "Networking", "Partnership", "Introduction"
        ])
    with col2:
        your_background = st.text_area("Your background", height=100)
        value_prop = st.text_area("What value do you bring?", height=100)

    if st.button("📧 Write Email", type="primary"):
        if recipient_role and purpose:
            with st.spinner("Writing your cold email..."):
                email = ask_claude(
                    f"Write a cold email for {purpose}.\n\n"
                    f"To: {recipient_role} at {company}\n"
                    f"My background: {your_background}\n"
                    f"Value I bring: {value_prop}\n\n"
                    f"Under 150 words, clear subject line, "
                    f"specific, strong call to action, not salesy."
                )
            st.markdown("### 📧 Your Cold Email:")
            st.markdown(email)

# ============================================
# PAGE: SALARY NEGOTIATION COACH
# ============================================
elif page == "💰 Salary Negotiation Coach":
    st.title("💰 Salary Negotiation Coach")
    st.subheader("Get scripts and strategies to negotiate your pay")

    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input("Job title",
            placeholder="e.g. AI Developer, IT Specialist...")
        location = st.text_input("Location", placeholder="e.g. Athens, GA")
        years_experience = st.selectbox("Years of experience", [
            "0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"
        ])
    with col2:
        current_offer = st.text_input("Current offer or salary",
            placeholder="e.g. $65,000")
        target_salary = st.text_input("Your target salary",
            placeholder="e.g. $80,000")
        situation = st.selectbox("Situation", [
            "Negotiating a new job offer", "Asking for a raise",
            "Counter offering after rejection", "Negotiating a promotion"
        ])

    if st.button("💰 Get Negotiation Strategy", type="primary"):
        if job_title and situation:
            with st.spinner("Building your negotiation strategy..."):
                strategy = ask_claude(
                    f"Create a salary negotiation strategy for:\n\n"
                    f"Role: {job_title} in {location}\n"
                    f"Experience: {years_experience}\n"
                    f"Current offer/salary: {current_offer}\n"
                    f"Target: {target_salary}\nSituation: {situation}\n\n"
                    f"Provide:\n1. Market rate research\n2. Realistic target range\n"
                    f"3. Word-for-word negotiation script\n4. Counter offer responses\n"
                    f"5. What NOT to say\n6. Non-salary perks to negotiate"
                )
            st.markdown("### 💰 Your Negotiation Strategy:")
            st.markdown(strategy)

# ============================================
# PAGE: LEARNING ROADMAP
# ============================================
elif page == "📚 Learning Roadmap":
    st.title("📚 Learning Roadmap")
    st.subheader("Get a personalized study plan for any tech skill")

    skill = st.text_input("What do you want to learn?",
        placeholder="e.g. Machine Learning, React, Cloud Computing...")
    current_level = st.selectbox("Your current level", [
        "Complete beginner", "Some basics", "Intermediate", "Advanced but rusty"
    ])
    time_available = st.selectbox("Time available per week", [
        "1-2 hours", "3-5 hours", "5-10 hours", "10+ hours"
    ])
    goal = st.text_input("Your goal",
        placeholder="e.g. Get a job, build a project, pass a cert...")

    if st.button("📚 Generate Roadmap", type="primary"):
        if skill:
            with st.spinner("Building your personalized roadmap..."):
                roadmap = ask_claude(
                    f"Create a learning roadmap for: {skill}\n\n"
                    f"Level: {current_level}\nTime/week: {time_available}\n"
                    f"Goal: {goal}\n\nInclude:\n"
                    f"1. Phase-by-phase plan with timeframes\n"
                    f"2. Best free and paid resources per phase\n"
                    f"3. Projects to build at each stage\n"
                    f"4. Milestones to measure progress\n"
                    f"5. Common mistakes to avoid"
                )
            st.markdown("### 📚 Your Learning Roadmap:")
            st.markdown(roadmap)

# ============================================
# PAGE: ERROR EXPLAINER
# ============================================
elif page == "🐛 Error Explainer":
    st.title("🐛 Error Explainer")
    st.subheader("Paste any error and get a plain English fix")

    error_message = st.text_area("Paste your error message", height=150)
    code_context = st.text_area("Paste the relevant code (optional)", height=150)
    language = st.selectbox("Language",
        ["Python", "JavaScript", "HTML/CSS", "SQL", "Other"])

    if st.button("🐛 Explain & Fix", type="primary"):
        if error_message:
            with st.spinner("Both AIs diagnosing your error..."):
                claude_response = ask_claude(
                    f"Explain this {language} error and fix it:\n\n"
                    f"Error: {error_message}\nCode: {code_context}\n\n"
                    f"Provide: 1) What caused it 2) How to fix it "
                    f"3) How to avoid it next time"
                )
                chatgpt_response = ask_chatgpt(
                    f"Fix this {language} error:\n\n"
                    f"Error: {error_message}\nCode: {code_context}\n\n"
                    f"Claude suggested:\n{claude_response}\n\n"
                    f"Add anything missing or an alternative fix."
                )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📘 Claude's Fix:")
                st.markdown(claude_response)
            with col2:
                st.markdown("### 📗 ChatGPT's Fix:")
                st.markdown(chatgpt_response)

# ============================================
# PAGE: CODE DOCUMENTER
# ============================================
elif page == "📖 Code Documenter":
    st.title("📖 Code Documenter")
    st.subheader("Get comments and documentation written for your code")

    code = st.text_area("Paste your code here", height=300)
    language = st.selectbox("Language",
        ["Python", "JavaScript", "HTML/CSS", "SQL", "Other"])
    doc_style = st.selectbox("Documentation style", [
        "Inline comments only", "Docstrings and comments",
        "Full README documentation", "All of the above"
    ])

    if st.button("📖 Document My Code", type="primary"):
        if code:
            with st.spinner("Writing documentation..."):
                documented = ask_claude(
                    f"Add {doc_style} to this {language} code:\n\n{code}\n\n"
                    f"Be thorough and helpful for someone learning the code."
                )
            st.markdown("### 📖 Documented Code:")
            st.markdown(documented)

# ============================================
# PAGE: PROMPT ENGINEER
# ============================================
elif page == "🎨 Prompt Engineer":
    st.title("🎨 Prompt Engineer")
    st.subheader("Write better AI prompts that get better results")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Your Current Prompt")
        weak_prompt = st.text_area("Paste your prompt here", height=200,
            placeholder="e.g. Write me a cover letter")
        ai_target = st.selectbox("Which AI is this prompt for?", [
            "Claude", "ChatGPT", "Both",
            "Image AI (Midjourney/DALL-E)", "Any AI"
        ])
        goal = st.text_input("What are you trying to achieve?",
            placeholder="e.g. Get a professional cover letter for a tech job")

    with col2:
        st.markdown("### Improved Prompt")
        if st.button("🎨 Improve My Prompt", type="primary"):
            if weak_prompt:
                with st.spinner("Engineering a better prompt..."):
                    result = ask_claude(
                        f"You are an expert prompt engineer. Improve this prompt:\n\n"
                        f"ORIGINAL: {weak_prompt}\n"
                        f"TARGET AI: {ai_target}\nGOAL: {goal}\n\n"
                        f"Provide:\n1. Improved version of the prompt\n"
                        f"2. What was weak about the original\n"
                        f"3. 3 prompt engineering tips used\n"
                        f"4. An advanced version with even more detail\n\n"
                        f"Explain WHY each improvement works."
                    )
                st.markdown(result)

    st.divider()
    st.markdown("### 💡 Prompt Engineering Quick Tips")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Be Specific**\nVague prompts get vague answers. Include context, format, length and tone.")
    with col2:
        st.info("**Give Examples**\nShow the AI what good output looks like with sample outputs.")
    with col3:
        st.info("**Assign a Role**\nStart with 'You are an expert in...' to get focused responses.")

# ============================================
# PAGE: APP IDEA VALIDATOR
# ============================================
elif page == "📱 App Idea Validator":
    st.title("📱 App Idea Validator")
    st.subheader("Get honest market feedback on your app idea")

    app_idea = st.text_area("Describe your app idea", height=150,
        placeholder="e.g. An AI platform that combines Claude and ChatGPT...")

    col1, col2 = st.columns(2)
    with col1:
        target_audience = st.text_input("Who is this for?",
            placeholder="e.g. College students, small business owners...")
        monetization = st.selectbox("How would you make money?", [
            "Subscription (monthly fee)", "One-time purchase",
            "Freemium (free + paid tier)", "Ads",
            "Per-use pricing", "Not sure yet"
        ])
    with col2:
        competitors = st.text_input("Any similar apps you know of?",
            placeholder="e.g. ChatGPT, Notion AI...")
        stage = st.selectbox("Where are you?", [
            "Just an idea", "Started planning",
            "Building prototype", "Ready to launch"
        ])

    if st.button("📱 Validate My Idea", type="primary"):
        if app_idea:
            with st.spinner("Both AIs analyzing your app idea..."):
                claude_analysis = ask_claude(
                    f"Analyze this app idea honestly:\n\n"
                    f"IDEA: {app_idea}\nAUDIENCE: {target_audience}\n"
                    f"MONETIZATION: {monetization}\nCOMPETITORS: {competitors}\n"
                    f"STAGE: {stage}\n\nProvide:\n"
                    f"1. Honest assessment (be direct, not just positive)\n"
                    f"2. Strongest aspects of the idea\n"
                    f"3. Biggest challenges and risks\n"
                    f"4. Competitive advantage needed to win\n"
                    f"5. Revenue potential estimate\n"
                    f"6. Top 3 recommended next steps\n"
                    f"7. Overall viability score out of 10"
                )
                chatgpt_analysis = ask_chatgpt(
                    f"Validate this app idea:\n\n"
                    f"IDEA: {app_idea}\nAUDIENCE: {target_audience}\n"
                    f"MONETIZATION: {monetization}\n\n"
                    f"Claude's analysis:\n{claude_analysis}\n\n"
                    f"Add a different perspective. Agree or disagree "
                    f"with Claude and explain why. What did Claude miss?"
                )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📘 Claude's Analysis:")
                st.markdown(claude_analysis)
            with col2:
                st.markdown("### 📗 ChatGPT's Take:")
                st.markdown(chatgpt_analysis)