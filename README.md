# AI Tool Calling Assistant 🔍🤖

An AI-powered assistant built using **LangChain, Google Gemini, and Tavily Search** that intelligently uses external tools to retrieve real-time information and generate relevant responses.

## 🚀 Project Overview

This project demonstrates the implementation of Tool Calling in Generative AI using LangChain.

The assistant receives a user query and uses Google Gemini to decide whether an external search tool is required. When current information is needed, it invokes Tavily Search, retrieves relevant results, and passes them back to Gemini to generate a final response.

## ✨ Features

- **Google Gemini Integration:** Uses Gemini as the underlying LLM.
- **Tool Calling:** Allows the LLM to decide when to use external tools.
- **Web Search:** Integrates Tavily Search to retrieve current information.
- **LangChain Pipeline:** Uses prompt templates and output parsers.
- **Environment Variables:** Securely manages API keys using dotenv.
- **Context-Based Responses:** Generates answers using retrieved search results.

## 🛠️ Technologies Used

- Python
- LangChain
- Google Gemini API
- Tavily Search API
- python-dotenv

## ⚙️ Project Workflow

1. Load environment variables using `load_dotenv()`.
2. Initialize the Tavily Search tool.
3. Initialize the Google Gemini model.
4. Bind the search tool with Gemini using `bind_tools()`.
5. Send the user's query through a prompt template.
6. Check whether Gemini requests a tool call.
7. Execute Tavily Search when required.
8. Pass search results back to Gemini.
9. Generate the final response.

## 📂 Project Structure

```text
AI-Tool-Calling-Assistant/
│
├── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## 📦 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/khayati628/newssummarizer
cd news-summarizer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get your API keys:

- Google AI Studio: https://aistudio.google.com/
- Tavily: https://tavily.com/

### 5. Run the project

```bash
python news-summarizer.py
```

## 💡 Example

**Input:**
```text
What are the latest updates on AI jobs this week?
```

**Execution:**
- Gemini analyzes the query.
- Gemini requests Tavily Search.
- Tavily retrieves relevant web results.
- Gemini generates a final answer using the search results.

## 🧠 Key Concepts Learned

- Large Language Models (LLMs)
- LangChain Tool Calling
- `bind_tools()`
- `tool_calls`
- Tool execution using `invoke()`
- ChatPromptTemplate
- StrOutputParser
- LLM pipelines

## 🔮 Future Improvements

- Integrate multiple tools into one assistant.
- Implement a proper agent execution loop.
- Add a Streamlit user interface.
- Improve conversation memory.
- Add source links and citations to search responses.

## 👩‍💻 Author

**Khyati Sharma**

B.Tech Computer Science Engineering

Interested in Artificial Intelligence, Machine Learning, Deep Learning, and Generative AI.
