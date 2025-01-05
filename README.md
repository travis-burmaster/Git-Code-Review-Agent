# Git Code Review Agent 🤖

An intelligent code review and fix agent powered by LangGraph and OpenAI. This tool automatically analyzes your repository, identifies issues, searches for solutions, and implements fixes - all while providing detailed explanations of its actions.

## Features ✨

- 🔍 **Automated Code Review**: Analyzes code quality, patterns, and potential issues
- 🛠️ **Automatic Fix Implementation**: Implements solutions for identified problems
- 🔎 **Solution Search**: Uses SerpAPI to find relevant documentation and best practices
- 📊 **Git Integration**: Full Git command support for repository analysis
- 📝 **Detailed Reporting**: Provides comprehensive explanations of all changes made

## Requirements 📋

- Python 3.8+
- OpenAI API key
- SerpAPI key
- Git installed and configured

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/travis-burmaster/Git-Code-Review-Agent.git
cd Git-Code-Review-Agent
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
python -m venv venv
source venv/bin/activate

pip install langgraph langchain-openai langchain-community

export OPENAI_API_KEY='your-openai-api-key'
export SERPAPI_API_KEY='your-serpapi-api-key'
```

## Usage 💻

### Basic Usage

```python
from code_review_agent import run_code_review

messages = run_code_review(
    user_input="Please review the code in src/main.py and fix any performance issues",
    repo_path="/path/to/your/repo",
    openai_api_key="your-openai-api-key",
    serpapi_api_key="your-serpapi-api-key"
)
```

### Example Commands

1. Review specific file:
```python
"Please review src/main.py for potential performance issues"
```

2. Analyze entire repository:
```python
"Perform a full repository review focusing on security best practices"
```

3. Fix specific issues:
```python
"Fix memory leaks in the data processing module"
```

## How It Works 🔄

1. **Request Analysis**: The agent processes your review request
2. **Repository Scan**: Checks repository status and relevant files
3. **Code Analysis**: Reviews code for issues and improvements
4. **Solution Search**: If needed, searches for best practices and solutions
5. **Fix Implementation**: Applies necessary changes
6. **Verification**: Verifies changes and their impact
7. **Reporting**: Provides detailed explanation of actions taken

## Configuration ⚙️

You can customize the agent's behavior by modifying the following parameters:

- Model selection (default: gpt-4-1106-preview)
- Temperature setting for response generation
- Custom tool configurations
- Git command preferences

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- OpenAI for their powerful language models
- LangGraph for the workflow framework
- SerpAPI for search capabilities
- All contributors who help improve this tool

## Support 💬

If you have any questions or run into issues, please open an issue in the GitHub repository.