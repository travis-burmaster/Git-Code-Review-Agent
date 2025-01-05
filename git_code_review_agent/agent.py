from typing import Dict, List, Tuple, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import Graph, StateGraph
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_community.tools.serpapi import SerpAPIWrapper
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
import subprocess
import os

class GitTools:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def execute_git_command(self, command: List[str]) -> str:
        try:
            result = subprocess.run(
                ['git'] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    def get_file_content(self, file_path: str) -> str:
        full_path = os.path.join(self.repo_path, file_path)
        try:
            with open(full_path, 'r') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file_content(self, file_path: str, content: str) -> str:
        full_path = os.path.join(self.repo_path, file_path)
        try:
            with open(full_path, 'w') as file:
                file.write(content)
            return "File updated successfully"
        except Exception as e:
            return f"Error writing file: {str(e)}"

def create_code_review_agent(repo_path: str, openai_api_key: str, serpapi_api_key: str):
    # Initialize tools
    git_tools = GitTools(repo_path)
    search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)

    # Define tools
    tools = [
        Tool(
            name="git_status",
            func=lambda: git_tools.execute_git_command(["status"]),
            description="Get the current git status of the repository"
        ),
        Tool(
            name="git_diff",
            func=lambda: git_tools.execute_git_command(["diff"]),
            description="Show changes in the working directory"
        ),
        Tool(
            name="read_file",
            func=lambda file_path: git_tools.get_file_content(file_path),
            description="Read the content of a file in the repository"
        ),
        Tool(
            name="write_file",
            func=lambda file_path, content: git_tools.write_file_content(file_path, content),
            description="Write content to a file in the repository"
        ),
        Tool(
            name="search_solution",
            func=search.run,
            description="Search the internet for code solutions and documentation"
        )
    ]

    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-4-1106-preview",
        temperature=0,
        api_key=openai_api_key
    )

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert code reviewer and fixer. 
        Your task is to:
        1. Review code in the git repository
        2. Identify issues and potential improvements
        3. Search for solutions when needed
        4. Implement fixes directly
        5. Provide clear explanations of changes made

        Follow these steps for each review:
        1. Check git status and diff
        2. Read relevant files
        3. Analyze the code
        4. Search for solutions if needed
        5. Implement fixes
        6. Verify changes
        7. Provide a summary of actions taken

        {agent_scratchpad}"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Define the nodes for the graph
    def analyze_request(state):
        messages = state["messages"]
        response = agent_executor.invoke({
            "input": messages[-1].content,
            "chat_history": messages[:-1],
            "agent_scratchpad": ""
        })
        return {
            "messages": messages + [AIMessage(content=response["output"])]
        }

    # Create the graph
    workflow = StateGraph(nodes=[analyze_request])

    # Define the edges
    workflow.add_edge("analyze_request", "analyze_request")

    # Set the entry point
    workflow.set_entry_point("analyze_request")

    # Compile the graph
    graph = workflow.compile()

    return graph

def run_code_review(
    user_input: str,
    repo_path: str,
    openai_api_key: str,
    serpapi_api_key: str
) -> List[str]:
    """
    Run the code review process with the given user input.
    
    Args:
        user_input: The user's request or description of the issue
        repo_path: Path to the git repository
        openai_api_key: OpenAI API key
        serpapi_api_key: SerpAPI key
    
    Returns:
        List of messages from the conversation
    """
    graph = create_code_review_agent(repo_path, openai_api_key, serpapi_api_key)
    
    # Initialize the state
    state = {
        "messages": [HumanMessage(content=user_input)]
    }
    
    # Run the graph
    for output in graph.stream(state):
        current_messages = output["messages"]
        if len(current_messages) > len(state["messages"]):
            latest_message = current_messages[-1].content
            print(f"Agent: {latest_message}")
        
        state = output
    
    return [msg.content for msg in state["messages"]]
