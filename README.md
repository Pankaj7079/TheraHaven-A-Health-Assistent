# TheraHaven – A Health Assistent

TheraHaven is a sophisticated AI-powered platform providing **confidential, empathetic, and immediate support** for anyone navigating mental health challenges. Designed by combining advanced language models, robust backend orchestration, and secure emergency features, TheraHaven ensures users have access to a caring companion that listens, helps, and acts when lives are at risk.

***

## What is TheraHaven?

TheraHaven uses natural language processing and cloud-based services to simulate a compassionate mental health professional. Whether you're struggling emotionally, seeking guidance, or in need of critical help, TheraHaven creates a safe and supportive digital space. It is **not a substitute for clinical care**, but serves as a bridge to personal reflection, professional resources, and immediate intervention in crisis situations.

***

## Project File Overview

Every file in TheraHaven's architecture is a modular building block enabling functionality, safety, and maintainability.

| File                | Core Purpose                                                        |
|---------------------|---------------------------------------------------------------------|
| **ai_agent.py**     | Defines how TheraHaven converses, detects emergencies, and routes queries using LangChain agents. Integrates specific tools for conversation, emergency response, and therapist recommendations.|
| **tools.py**        | Implements MedGemma (AI therapist), Twilio emergency calling, and therapist locator tools. Enforces principles for empathetic, strengths-focused dialogue.|
| **config.py**       | Manages all sensitive environment variables (API keys, phone numbers) securely using `dotenv`. Enables seamless cloud integrations.|
| **main.py**         | Powers the FastAPI backend, receiving user input, detecting emergencies, invoking the AI agent, and returning structured responses.|
| **frontend.py**     | Hosts the Streamlit web app for user interaction. Presents an accessible interface connected to backend APIs and models.|
| **pyproject.toml**  | Python project and dependency management via Poetry. Ensures precise reproducibility and easy installation.|
| **.env**            | Stores private credentials, never committed to version control.|
| **.gitignore**      | Keeps sensitive and build files out of Git repositories.|
| **.python-version** | Specifies required Python (>=3.12) for environment consistency.|
| **uv.lock**         | Poetry lockfile for consistent dependency resolution.|
| **README.md**       | Documentation guiding developers, contributors, and users.|

***

## System Features & Safety

- **Empathetic AI Conversations**: Powered by LangChain and MedGemma, TheraHaven simulates a compassionate psychologist who listens, validates, and gently guides through open-ended dialogue. The agent adapts its empathy level, normalizes feelings, and supports strengths-led journeys.
- **Immediate Emergency Response**: At any sign of suicidal thoughts or crisis keywords, TheraHaven instantly initiates an emergency call via Twilio—*without hesitation, questions, or alternative responses*. The user's safety is the highest priority.
- **Therapist Locator Utility**: Connects users to real, licensed therapists when requested, and can provide contact details based on location.
- **Privacy and Security**: All configurations are loaded securely from environment files. No sensitive user data is stored.
- **Robust Backend and Frontend**: FastAPI handles all requests, session management, and validation. Streamlit offers a user-friendly and responsive web interface.
- **Modular Design**: Each system layer is independently testable, extendable, and documented for future growth (e.g., add more specialists or resource modules).

***

## Technology Highlights

- **AI/ML**: LangChain, LangChain-Groq, Ollama, MedGemma, LangGraph
- **Backend**: FastAPI, Python >=3.12
- **Frontend**: Streamlit
- **Communication**: Twilio API
- **Configuration**: dotenv for secure variable handling
- **Location & Resources**: Geocoder, therapist-locator integrations
- **Quality Control**: Poetry and lockfiles for exact dependency versions

***

## Fast Start Guide
 1. **Start Backend & Frontend**
   ```bash
   uv run python Backend/main.py
   uv run streamlit run frontend.py
   # Visit http://localhost:8501
   ```

***

## Clinical Intelligence and Ethics

- Empathy, normalization, and strengths-focus are at the core—mirroring best practices from real psychologists (as implemented in MedGemma system prompts).
- The agent will **always act immediately if self-harm is detected**, never requesting clarification—saving crucial time in crisis situations.
- Conversations are designed to empower users, never dictate, and always validate feelings.

 
***

TheraHaven is dedicated to supporting *real people* in *real situations* through AI-powered empathy and immediate action. For emergencies, always seek professional help. TheraHaven is here to guide, support, and connect—when you need it most.


to run frontend use
 uv run python -m streamlit run frontend.py
>>

  You can now view your Streamlit app in your browser.