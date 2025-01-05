from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="git-code-review-agent",
    version="0.1.0",
    author="Travis Burmaster",
    author_email="travis.burmaster@example.com",
    description="An intelligent code review and fix agent using LangGraph and OpenAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/travis-burmaster/Git-Code-Review-Agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "code-review=code_review_agent:main",
        ],
    },
)