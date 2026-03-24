# Guided Navigation Web Extension

Guided Navigation is a system that enables users to control and automate web interactions using a **chatbot-style interface**.

Instead of manually navigating webpages, users can give **natural language commands**, and an AI-powered backend interprets them and performs actions such as clicking elements, searching content, checking checkboxes, and submitting forms.

The system combines a **Chrome Extension frontend** with a **Python LangGraph-powered AI backend** to enable intelligent browser automation.

Future versions will support: 
- **LLM-generated JavaScript execution** – dynamically generate and embed JavaScript scripts based on user commands and execute them directly within the Chrome extension for more flexible webpage automation.
- support **speech-based interaction**, allowing users to control webpages using voice commands.

## Features

* Chat-based interface for webpage interaction
* Click buttons and links using commands
* Search within webpages
* Check / uncheck checkboxes
* Fill and submit forms (login, signup, etc.)
* AI agent decision making using **LangGraph**
* Real-time browser automation
* Upcoming **LLM-generated JavaScript execution**
* Upcoming **voice-based navigation**

## Architecture Overview

```
User Command
↓
Chrome Extension (UI + DOM Access)
↓
Backend API
↓
LangGraph Workflow (LLM reasoning + tool orchestration)
↓
Action Executor
↓
DOM Interaction
```

## Tech Stack

Frontend (Extension)

* JavaScript
* Chrome Extension APIs
* HTML / CSS

Backend

* Python
* LangGraph
* LLM integration
* FastAPI / API routes

## Project Structure
```
guided-navigation/
│
│   ├── app/
│   │   ├── agents/        # Agent logic
│   │   ├── config/        # Configuration files
│   │   ├── constants/     # Global constants
│   │   ├── exceptions/    # Custom exceptions
│   │   ├── graph/         # LangGraph workflows
│   │   ├── llms/          # LLM integrations
│   │   ├── logs/          # Logging
│   │   ├── prompts/       # Prompt templates
│   │   ├── routes/        # API endpoints
│   │   ├── tools/         # Action tools for agents
│   │   ├── __init__.py
│   │   └── main.py        # Backend entry point
│
│   ├── extension/         # Chrome extension source
│
│   ├── .env.example
│   ├── .gitignore
│   └── .dockerignore
│
└── README.md
```

## Setup & Installation

1. Clone the Repository

* git clone https://github.com/mfsi-garimas/guided-navigation-updated.git
* cd guided-navigation

2. Backend Setup (Python)

	Create a virtual environment

		python -m venv .venv

	Activate environment

		Mac/Linux:

		source .venv/bin/activate

		Windows:

		.venv\Scripts\activate

3. Install dependencies

	pip install -r requirements.txt

4. Add environment variables

	cp .env.example .env

5. Run backend server

	python app/main.py

## Chrome Extension Setup

1. Open Chrome and navigate to

	chrome://extensions/

2. Enable **Developer Mode**

3. Click **Load Unpacked**

4. Select the `extension` folder

The extension will now be available in your browser.

## Configure API Base URL

The extension requires a BASE_URL to communicate with the backend API.

When the extension runs for the first time, it will prompt you to enter the API base URL.

Example:

http://127.0.0.1:8001/api

This value is stored using Chrome local storage and will be reused in future sessions.

Note: The code that handles this prompt and storage is located in extension/content/config.js. You can inspect or modify it there if needed.

## How to remove BASE_URL:

1. Open Chrome DevTools on any webpage (where the extension runs).

2. Go to the Application tab.

3. Expand Storage → Extension storage → [Your Extension Name] → Local.

4. Find the BASE_URL key in the right panel.

5. Right-click it and choose Delete or select it and press the Delete key.

## Usage

1. Open any webpage.
2. Click the extension icon.
3. Enter a command in the chatbot.

Example commands:

```
Go to get certified
search for java tutorials
login with username test and password 123
```

The AI agent will interpret the command and perform the action on the webpage.

## Future Improvements

* LLM-generated JavaScript execution – dynamically generate and embed JavaScript scripts based on user commands and execute them directly within the Chrome extension for more flexible webpage automation
* Voice-based navigation