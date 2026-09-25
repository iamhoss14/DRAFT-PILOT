# DRAFT-PILOT ✍️

A full-stack, AI-powered micro-SaaS application designed to generate high-quality, perfectly formatted content instantly.

DRAFT-PILOT separates a robust **FastAPI backend** from a sleek **Streamlit frontend**, utilizing Google's **Gemini 3.8 Flash** model to generate articles, emails, strategic briefs, and social media posts.

---

## ✨ Features

* **Decoupled Architecture:** Clean separation of concerns with a FastAPI backend handling business logic and a modern Streamlit UI for the frontend.
* **Advanced Gemini Integration:** Powered by Google's `gemini-3.8-flash` model through the latest `google-genai` SDK.
* **Resilient Error Handling:** Built-in automatic retry mechanisms for gracefully handling temporary `503` server congestion.
* **Smart Rate Limiting:** Custom in-memory IP rate limiter restricting users to a defined number of requests per day to protect API quotas.
* **Proxy Support:** Supports routing traffic through local SOCKS5 proxies for environments where direct API access may be restricted.
* **Modern UI/UX:** Responsive, dark/light-mode compatible frontend with dynamic loading states and clean typography.

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### Frontend

* Streamlit
* Requests

### AI / LLM

* Google GenAI SDK
* Gemini 3.8 Flash

### Environment & Networking

* `python-dotenv`
* `httpx[socks]`

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/iamhoss14/DRAFT-PILOT.git
cd DRAFT-PILOT
```

### 2. Set Up the Virtual Environment

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file in the root directory of the project:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your Google AI Studio API key.

> **Important:** Never commit your `.env` file to GitHub. Add it to `.gitignore` to keep your API key private.

Example `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Running the Application

The backend and frontend must run simultaneously in two separate terminal windows.

### Terminal 1: Backend

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the FastAPI server:

```bash
./venv/bin/uvicorn app.main:app --reload
```

The FastAPI backend will be available at:

```text
http://127.0.0.1:8000
```

---

### Terminal 2: Frontend

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the Streamlit application:

```bash
streamlit run app/ui.py
```

The Streamlit frontend will be available at:

```text
http://localhost:8501
```

---

## 🏗️ Architecture

DRAFT-PILOT follows a decoupled frontend/backend architecture:

```text
                    User
                      │
                      ▼
             ┌─────────────────┐
             │ Streamlit UI    │
             │   Frontend      │
             └────────┬────────┘
                      │
                 HTTP Requests
                      │
                      ▼
             ┌─────────────────┐
             │    FastAPI      │
             │    Backend      │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Google Gemini   │
             │   AI Model      │
             └─────────────────┘
```

The Streamlit frontend is responsible for user interaction, while the FastAPI backend handles API requests, business logic, rate limiting, and communication with the Gemini API.

---

## 🗺️ Roadmap

Upcoming features and improvements:

* [ ] **Database Integration:** Implement PostgreSQL to permanently store generated content and user history.
* [ ] **Data Analytics:** Integrate Pandas to analyze content generation trends and request volumes.
* [ ] **MLOps Foundations:** Add detailed performance logging, latency tracking, monitoring, and advanced prompt versioning.
* [ ] **User Authentication:** Replace IP-based rate limiting with secure JWT-based user accounts.
* [ ] **Content History:** Allow users to view and manage previously generated content.
* [ ] **Prompt Templates:** Provide predefined templates for common content-generation workflows.
* [ ] **Production Deployment:** Deploy the backend and frontend using production-ready infrastructure.

---

## 🔐 Security

DRAFT-PILOT uses environment variables for sensitive configuration such as API keys.

Never expose your Gemini API key directly in source code.

Before committing your project, make sure `.env` is included in `.gitignore`:

```text
.env
```

---

## 👨‍💻 Author

**Amirhossein Afzali**

* GitHub: [@iamhoss14](https://github.com/iamhoss14)

---

## 📄 License

This project is currently intended for educational and development purposes.
