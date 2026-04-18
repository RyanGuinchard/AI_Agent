# 🤖 AI Agent Code Editor (Boot.dev)

A Python project exploring the fundamentals of LLM-powered agents. This project implements a feedback loop using the Google Gemini API to interact with code and solve programming tasks.

## 📝 Project Overview
This is an experimental code assistant built to understand how AI agents function under the hood. Unlike a standard chatbot, this script utilizes **function calling** to bridge the gap between text generation and system execution.

The core objective is to build a "Think-Act-Observe" loop where the LLM can:
1. **Analyze** a codebase or bug.
2. **Execute** specific Python functions to inspect or modify files.
3. **Learn** from the output of its own actions to iterate on a solution.

## 🧪 Key Concepts
* **LLM Integration:** Connecting to Gemini via the `google-genai` library.
* **Function Calling:** Defining tools that allow the LLM to interact with the local filesystem.
* **Feedback Loops:** Passing the results of code execution back to the model to enable self-correction.

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Model:** Google Gemini
* **Package Manager:** [uv](https://github.com/astral-sh/uv)
* **Libraries:** * `google-genai==1.12.1`
    * `python-dotenv==1.1.0`
