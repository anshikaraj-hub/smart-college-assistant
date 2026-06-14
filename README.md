# Smart College Assistant

An AI-powered college assistant using LangChain's Tool Calling Agent. It automatically identifies the type of student query and invokes the correct tool to compute the answer.

## Tools
- Attendance Calculator
- Result Calculator (Average, Grade, Pass/Fail)
- Fee Balance Calculator
- Library Fine Calculator
- Hostel Fee Calculator
- Student Information Tool (bonus)

## Tech Stack
- Python
- LangChain (langchain_classic agents)
- Ollama (llama3.2) — local LLM, no API key needed

## Setup
1. Install [Ollama](https://ollama.com) and pull a model:
```bash
ollama pull llama3.2
```
2. Install dependencies:
```bash
pip install langchain langchain-classic langchain-ollama langchain-core
```
3. Run:
```bash
python college_assistant.py
```

## Usage
The script runs the assignment's required test cases first (with `verbose=True` showing the agent's reasoning), then enters an interactive mode where you can type your own queries.

## Status
✅ Assignment complete — pending final polish.
