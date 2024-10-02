# DrWU AI Customer Service Chatbot

![DrWU AI Assistant](demo/DrWU.mp4)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Overview

DrWU AI Customer Service Chatbot leverages **LangChain**, **OpenAI**, and **VertexAI** to deliver an intelligent and responsive customer service experience. The application consists of a FastAPI backend and a React-based frontend, enabling seamless interaction through a web-based chat interface.

## Features

- **Intelligent Responses:** Utilizes LangChain and OpenAI's language models to understand and respond to user queries effectively.
- **Data Integration:** Integrates with VertexAI for enhanced data processing and retrieval.
- **Web-Based Interface:** Provides a user-friendly chat interface built with React.
- **Persistent Chat History:** Maintains chat history using local storage for continuous user experience.
- **Dockerized Deployment:** Easily deployable using Docker for consistent environments.

## Architecture

The chatbot's architecture is designed to handle user interactions efficiently by combining several advanced technologies:

1. **LangChain Pipeline:**

- **LLM Initialization:** Sets up the language model for processing.
- **Intent Recognition:** Determines the user's intent from their question.
- **Document Retrieval:** Fetches relevant product documents from the database.
- **Ensemble Retriever:** Combines multiple retrieval strategies for accuracy.
- **Response Generation:** Constructs a coherent and informative response based on the retrieved data.

2. **Data Management:**

- **create_data.py:** Scrapes official website data and populates the databases (`products.db`, `product_details.db`, `product_vertex.db`).

3. **Backend:**

- **FastAPI:** Serves API endpoints for handling chat requests and serving static files.
- **LangChain Utils:** Manages the interaction between LangChain, OpenAI, and VertexAI.

4. **Frontend:**

- **React (chat.js):** Provides an interactive chat interface within an HTML page.
- **Templates and Static Files:** Includes HTML templates and CSS for styling the chat interface.

## Project Structure

```bash
drwu
├── .gitignore
├── config.py
├── create_data.py
├── Dockerfile
├── db
│   ├── products.db
│   ├── product_details.db
│   └── product_vertex.db
├── del__pycache__.py
├── demo
│   └── DrWU.mp4
├── etc
│   └── secrets
│       ├── google_adc.json
│       └── google_api.json
├── langchain_utils
│   ├── main.py
│   ├── step_1.py
│   ├── step_2.py
│   ├── step_3.py
│   ├── step_4.py
│   ├── step_5.py
│   ├── step_6.py
│   └── __init__.py
├── LICENSE.txt
├── main.py
├── README.md
├── requirements.txt
├── static
│   ├── chat.js
│   └── styles.css
├── templates
│   └── chat.html
├── test.py
├── utils
│   ├── product_details.py
│   ├── product_vertex.py
│   ├── scrape_details.py
│   └── scrape_products.py
├── utils_vertexai
│   ├── chat_input.py
│   ├── generative_model_wrapper.py
│   └── __init__.py
└── web
    └── druw.html
```

## Installation

### Prerequisites

- **Python 3.8+**
- **Docker** (optional, for containerized deployment)
- **Node.js and npm** (for frontend development)

### Steps

1. **Clone the Repository:**

```bash
git clone https://github.com/yourusername/drwu.git
cd drwu
```

2. **Set Up Virtual Environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

create `config.py`
```python
import os
class Config:
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    BIGQUERY_PROJECT_ID = os.getenv('BIGQUERY_PROJECT')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure Secrets:**

- Place your `google_adc.json` and `google_api.json` in the `etc/secrets/` directory.

5. **Populate the Database:**

```bash
python create_data.py
```

6. **Build and Run with Docker (Optional):**

```bash
docker build -t drwu .
docker run -d -p 8000:8000 drwu
```

## Usage

1. **Run the Application:**

```bash
uvicorn main:app --reload
```

- The application will be accessible at 
    1. [http://127.0.0.1:8000](http://127.0.0.1:8000)
    2. [http://127.0.0.1:8000/web/druw.html](http://127.0.0.1:8000/web/druw.html)

2. **Interact with the Chatbot:**

- Open the URL in your browser.
- Enter your questions in the chat interface.
- The chatbot will respond based on the integrated LangChain pipeline.

## License

This project is licensed under the [MIT License](LICENSE.txt).

---

For any issues or contributions, please open an issue or submit a pull request on the [GitHub repository](https://github.com/NyannNya/drwu).
