# Intelligent Core AI
A Tkinter-based chatbot powered by Gemini 2.5 Flash.

# About
Intelligent Core AI is a sleek, multi-threaded desktop assistant built using Python and Tkinter. This project is fully driven by the official Google GenAI SDK (gemini-2.5-flash), meaning all conversational logic is handled dynamically by the AI model using custom system instructions rather than hardcoded rules.

Key features include an automated workspace environment to switch between conversation threads, seamless mouse-wheel scroll integration for smoother UI navigation, dynamic system theme switching (Dark & Light modes), and a fully secure architecture that reads credentials safely from environment variables to prevent API key exposure on public platforms.

## Setup Instructions
1. Install dependencies: `pip install google-genai python-dotenv`
2. Create a `.env` file and add your key: `GEMINI_API_KEY=your_key_here`
3. Run the app: `python Intelligent_Core_AI.py`
