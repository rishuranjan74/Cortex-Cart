import streamlit as st
import os
from dotenv import load_dotenv

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.agents import Tool, create_react_agent, AgentExecutor

# Web scraping imports
import requests
from bs4 import BeautifulSoup

# --- 1. SETUP ---

# Load environment variables from .env file
load_dotenv()

# Check for Brave API Key
if not os.environ.get("BRAVE_API_KEY"):
    st.error("BRAVE_API_KEY is not set. Please add it to your .env file.")
    st.stop()

# --- 2. TOOL DEFINITIONS ---

# Tool 1: Brave Search for finding product URLs
# This is a pre-built tool from the langchain-brave-search library
try:
    from langchain_brave_search import BraveSearch
    
    # Initialize the search tool. `k=5` means it will return the top 5 results.
    search_tool = BraveSearch.from_api_key(api_key=os.environ["BRAVE_API_KEY"], k=5)

except ImportError:
    st.error("Could not import BraveSearch. Please run 'pip install langchain-brave-search'.")
    st.stop()


# Tool 2: Web Scraper for extracting product details
def scrape_website(url: str) -> str:
    """
    Scrapes the text content of a given URL. Focuses on relevant tags
    like p, h1, h2, h3, and li to get product information and reviews.
    """
    print(f"\n[Scraping Tool]: Accessing URL: {url}\n")
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status() # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all relevant text elements
        texts = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'span'])
        
        # Extract and clean text, filtering out short/irrelevant snippets
        content = " ".join(text.get_text(strip=True) for text in texts if len(text.get_text(strip=True)) > 20)
        
        if not content:
            return "Scraping resulted in no meaningful content. The page might be JavaScript-heavy or empty."
            
        print(f"[Scraping Tool]: Successfully extracted {len(content)} characters of content.")
        # Return a manageable chunk of text to not overwhelm the LLM
        return content[:4000]

    except requests.RequestException as e:
        print(f"[Scraping Tool]: Error accessing {url}: {e}")
        return f"Error: Could not access the URL. {e}"
    except Exception as e:
        print(f"[Scraping Tool]: An unexpected error occurred during scraping: {e}")
        return f"Error: An unexpected error occurred while scraping. {e}"

# Instantiate the scraping tool for the agent
scrape_tool = Tool(
    name="WebScraper",
    func=scrape_website,
    description="A tool to scrape the text content of a given URL. Use this to get product details, specifications, and user reviews from the URLs provided by the Search tool."
)

# Combine all tools into a list for the agent
tools = [search_tool, scrape_tool]

# --- 3. AGENT AND LLM SETUP ---

# Initialize the local LLM (Ollama with Llama 3)
try:
    llm = Ollama(model="llama3")
except Exception as e:
    st.error(f"Failed to initialize Ollama LLM. Is Ollama running? Error: {e}")
    st.stop()


# Define the agent's prompt template. This is the core instruction set.
prompt_template = """
You are Cortex Cart, a friendly and expert AI Personal Shopper.
Your goal is to help the user find the perfect product based on their needs.
You must think step-by-step and use the available tools to gather information.

Here is the user's request: {input}

You have access to the following tools:
{tools}

**Thought Process:**
1.  **Understand the Request:** First, I need to break down the user's request. What is the product they are looking for? Are there any specific features, brands, or a budget mentioned?
2.  **Search for Products:** I will use the 'Search' tool to find relevant product pages, blogs, or review sites. My search query should be concise and based on the key terms from the user's request.
3.  **Analyze Search Results:** I will review the titles and snippets from the search results to identify the most promising URLs. I should prioritize URLs that seem to be product pages, trusted review sites, or direct e-commerce listings.
4.  **Scrape for Details:** For the 2-3 most promising URLs, I will use the 'WebScraper' tool to extract detailed information. I'm looking for product specifications, features, pricing, and, most importantly, user reviews or expert opinions.
5.  **Synthesize and Recommend:** After gathering all the information, I will synthesize it into a clear, concise, and helpful recommendation. I will explain *why* I am recommending a particular product, citing the information I found (e.g., "reviewers mentioned its great battery life"). I will present my final answer directly to the user in a conversational tone.

Begin!

{agent_scratchpad}
"""

# Create the prompt from the template
prompt = PromptTemplate.from_template(prompt_template)


# Create the ReAct (Reasoning and Acting) agent
agent = create_react_agent(llm, tools, prompt)

# Create the agent executor, which runs the agent's reasoning loop
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


# --- 4. STREAMLIT UI ---

st.set_page_config(page_title="Cortex Cart | Your AI Shopper", page_icon="🛒")

st.title("🛒 Cortex Cart")
st.caption("Your Personal AI Shopping Assistant, powered by Llama 3")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if user_query := st.chat_input("e.g., Find me the best noise-cancelling headphones under $300"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_query)

    # Display agent's response
    with st.chat_message("assistant"):
        with st.spinner("Cortex is thinking..."):
            try:
                response = agent_executor.invoke({"input": user_query})
                st.markdown(response['output'])
                # Add agent response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response['output']})
            except Exception as e:
                error_message = f"An error occurred: {e}. The agent might have had trouble with a website or the LLM. Please try rephrasing your query."
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
