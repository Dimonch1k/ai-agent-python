# Local AI Task Agent Framework

An autonomous, stateful local AI agent orchestrator built in Python using **LangGraph** and powered completely offline by **Ollama (Llama 3.1)**. This agent runs advanced multi-step system workflows by executing shell commands and parsing file systems.

## 🛠️ Integrated Native Tools
* **Terminal Engine Node:** Executes shell commands natively on the host machine to handle installations or checks.
* **File Management System:** Reads, writes, and appends data structures cleanly to files.
* **Graph Control Loop:** Powered by structured state charts to determine runtime paths safely without infinite recursion loops.

## 🚀 Quick Start Guide

### 1. Engine Dependencies
Ensure you have [Ollama installed](https://ollama.com) and the processing model downloaded:
```bash
ollama pull llama3.1
```

### 2. Local Setup
Sync your virtual environment and install project dependencies declared directly in your `pyproject.toml` file:
```bash
uv sync
```

### 3. Usage
Fire up the central agent interface loop:
```bash
python main.py
```

### Test Prompts to Validate Performance:
```bash
Create a new file tracking system properties named system_info.log containing my computer disk usage info.
```
```bash
Write a simple test script called hello.py that prints a custom text message, and then execute it via terminal commands to show me the result.
```

## ⚠️ Security Policy
This agent executes script variations directly on your host machine system shell. Do not link this instance to public exposed endpoints or run destructive global strings without enclosing it inside secure container wrappers like Docker.
