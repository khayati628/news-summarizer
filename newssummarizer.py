import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


search_tool = TavilySearchResults(max_results=2)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite", 
    temperature=0
)
llm_with_tools = llm.bind_tools([search_tool])


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use your tools when necessary to look up current information."),
    ("human", "{input}")
])


def run_assistant(query: str):
    chain = prompt | llm_with_tools
    response = chain.invoke({"input": query})
    
    
    if response.tool_calls:
        
        tool_call = response.tool_calls[0]
        print(f"\n[LLM triggered Tool]: {tool_call['name']}")
        
        
        search_query = tool_call['args'].get('query', query)
        
        
        tool_output = search_tool.invoke(search_query)
        
        
        final_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the user's question using the provided search results.\nSearch Results: {results}"),
            ("human", "{input}")
        ])
        
        final_chain = final_prompt | llm | StrOutputParser()
        final_answer = final_chain.invoke({"input": query, "results": tool_output})
        return final_answer
    else:
        return response.content

if __name__ == "__main__":
    user_query = "What are the latest updates on AI jobs from this week?"
    print(f"User Question: {user_query}")
    
    answer = run_assistant(user_query)
    print(f"\nFinal Answer:\n{answer}")