
import os
import streamlit as st

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.output_parsers import StrOutputParser


# 1. Page configuration
st.set_page_config(
    page_title="AI Search Assistant",
    page_icon="🤖",
    layout="centered"
)

# 2. Load environment variables
load_dotenv()

# 3. Initialize tools and model
@st.cache_resource
def initialize_assistant():

    search_tool = TavilySearchResults(max_results=2)

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0
    )

    llm_with_tools = llm.bind_tools([search_tool])

    return llm, llm_with_tools, search_tool


try:
    llm, llm_with_tools, search_tool = initialize_assistant()
except Exception as e:
    st.error(f"Initialization error: {e}")
    st.stop()


# 4. Prompt template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant. "
        "Use the Tavily search tool whenever current information is needed."
    ),
    ("human", "{input}")
])


# 5. Assistant execution logic
def run_assistant(query):

    chain = prompt | llm_with_tools

    response = chain.invoke({"input": query})

    search_used = False
    search_query = None

    # Check whether Gemini wants to use a tool
    if response.tool_calls:

        messages = [
            SystemMessage(
                content="You are a helpful assistant. "
                "Answer using the provided search results."
            ),
            HumanMessage(content=query),
            response
        ]

        for tool_call in response.tool_calls:

            if tool_call["name"] == search_tool.name:

                search_used = True

                search_query = tool_call["args"].get(
                    "query", query
                )

                # Execute Tavily search
                tool_output = search_tool.invoke(search_query)

                # Send tool result back to Gemini
                messages.append(
                    ToolMessage(
                        content=str(tool_output),
                        tool_call_id=tool_call["id"]
                    )
                )

        # Generate final response
        final_response = llm.invoke(messages)

        answer = StrOutputParser().invoke(final_response)

        return answer, search_used, search_query

    return response.content, search_used, search_query


# 6. Streamlit UI
st.title("🤖 AI Search Assistant")

st.markdown(
    "### Powered by Google Gemini + LangChain + Tavily"
)

st.caption(
    "Ask anything. Gemini can search the web when current "
    "information is required."
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:

    st.header("⚙️ Settings")

    st.write("**LLM:** Google Gemini")

    st.write("**Tool:** Tavily Search")

    st.write("**Framework:** LangChain")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []
        st.rerun()


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("search_used"):

            st.caption(
                f"🔎 Web search used: {message['search_query']}"
            )


# User input
user_query = st.chat_input("Ask me anything...")


if user_query:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("🤔 Gemini is thinking..."):

            try:

                answer, search_used, search_query = (
                    run_assistant(user_query)
                )

                st.markdown(answer)

                if search_used:

                    st.success("🔎 Tavily Search Tool Triggered")

                    st.caption(
                        f"Search query: {search_query}"
                    )

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "search_used": search_used,
                    "search_query": search_query
                })

            except Exception as e:

                st.error(f"Something went wrong: {e}")
