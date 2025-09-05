# Cortex-Cart

🛒 Cortex Cart: Your Personal AI Shopping Assistant
Cortex Cart is an advanced, conversational AI agent designed to act as a personal shopper. Powered by a locally-hosted Large Language Model (Llama 3), it understands your shopping needs in natural language, scours the web for real-time product information, summarizes user reviews, and provides intelligent, data-driven recommendations.

(Replace this placeholder with a screenshot of your running application)

✨ Core Features
🤖 Agentic AI Core: Utilizes a sophisticated agentic framework (LangChain) to reason, plan, and execute multi-step tasks autonomously.

🌐 Live Web Search: Integrates with the Brave Search API to find the most current product listings, review articles, and e-commerce pages.

📄 Intelligent Web Scraping: Employs BeautifulSoup4 to dynamically scrape and extract key information—specifications, pricing, and user reviews—from web pages.

🧠 Retrieval-Augmented Generation (RAG): Synthesizes unstructured text from multiple reviews into a concise summary of pros and cons, augmenting the LLM's knowledge for a final, nuanced recommendation.

💬 Conversational UI: A clean, user-friendly chat interface built with Streamlit for intuitive interaction.

🔒 Private & Local: Runs on a self-hosted LLM (Llama 3 via Ollama), ensuring your conversations are private and not reliant on cloud-based API providers.

🏗️ Technical Architecture
The application operates on a client-server model where the Streamlit UI communicates with the LangChain agent, which in turn leverages a locally running Ollama server for its core intelligence.

Frontend (Streamlit): Captures user queries and displays the agent's final response.

Backend (LangChain Agent): The core orchestration layer. It parses the user's request, plans a sequence of actions, and executes the necessary tools.

Reasoning Engine (Ollama & Llama 3): The agent's "brain." The LangChain agent sends prompts to the local Llama 3 model to decide which tool to use next or to synthesize a final answer.

Tools (Brave Search & Web Scraper): The agent's "hands." These tools interact with the outside world to gather the raw data needed to fulfill the user's request.

🛠️ Tech Stack
Category

Technology

AI / LLM

LangChain, Ollama, Llama 3

Web Interface

Streamlit

Data Tools

langchain-brave-search, BeautifulSoup4, requests

Language

Python 3.10+

Environment

python-dotenv

🚀 Getting Started
Follow these steps to set up and run Cortex Cart on your local machine.

1. Prerequisites
Python 3.10 or higher.

Ollama: You must have Ollama installed and running. Download it from ollama.com.

Git: Required for cloning the repository.

2. Installation & Setup
Step 1: Clone the Repository

git clone [https://github.com/your-username/cortex-cart.git](https://github.com/your-username/cortex-cart.git)
cd cortex-cart

Step 2: Set Up a Python Virtual Environment

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS / Linux
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Configure Environment Variables

Create a file named .env in the root of the project.

Get a free API key from the Brave Search API.

Add your API key to the .env file:

BRAVE_API_KEY="YOUR_BRAVE_SEARCH_API_KEY_HERE"

3. Running the Application
Step 1: Start the Ollama Server & Download Llama 3
Open a new terminal window and run the following command. This will download the Llama 3 model (if you don't have it already) and start the server.
You must leave this terminal running in the background.

ollama run llama3

Note: This requires at least 8GB of free RAM. It may be slow on machines without a dedicated GPU.

Step 2: Launch the Streamlit Application
In your original terminal (where you activated the venv), run the main application script:

streamlit run cortex_cart_app.py

Your default web browser will automatically open a new tab with the Cortex Cart application interface.

LICENSE
This project is licensed under the MIT License. See the LICENSE file for details.
