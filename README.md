# LangChain Chains

A collection of small, runnable examples showing how to build chains with
LangChain. Each example is designed to stand on its own so you can read one
file, run it, and understand how the chain is assembled.

## Planned topics

- A basic prompt → model → parser chain
- Sequential chains, where one step feeds the next
- Parallel chains that run several steps on the same input
- Routing an input to different prompts
- Retrieval chains that answer questions from a small document set
- Conversation chains that retain prior turns
- Structured output, where the model returns a validated object

## Prerequisites

Before setting up the project, install:

- [Git](https://git-scm.com/downloads)
- [Python 3.10 or newer](https://www.python.org/downloads/)
- An API key for the model provider used by the examples

Verify your Git and Python installations:

```bash
git --version
python --version
```

On some macOS and Linux systems, use `python3` and `pip3` instead of `python`
and `pip`.

## Local setup

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/BhanuRajpoot/Langchain-chains.git
   cd Langchain-chains
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment.

   **Windows (PowerShell):**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **Windows (Command Prompt):**

   ```bat
   .venv\Scripts\activate.bat
   ```

   **macOS/Linux:**

   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies after `requirements.txt` has been added:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. After `.env.example` has been added, create your local environment file:

   **Windows (PowerShell):**

   ```powershell
   Copy-Item .env.example .env
   ```

   **macOS/Linux:**

   ```bash
   cp .env.example .env
   ```

   Open `.env` and add the required API key. The `.env` file is ignored by
   Git and must never be committed.

## Running an example

From the repository root, with the virtual environment active, run:

```bash
python examples/<example_name>.py
```

Each example will load its settings, call the configured model, and print the
result.

## Project status

This repository is currently a starter project. Example scripts,
`requirements.txt`, and `.env.example` will be added as the project grows.

The planned project structure is:

```text
.
├── examples/          # One chain example per file
├── .env.example       # Environment variable names only
├── .gitignore
├── requirements.txt
└── README.md
```
