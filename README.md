# ✨ DraftPilot

DraftPilot is a production-oriented, AI-powered copywriting suite designed to generate, manage, and archive publication-ready content.

It goes beyond a simple LLM wrapper by combining structured prompt architecture with persistent PostgreSQL storage, allowing users to generate content based on specific types, tones, languages, and length requirements.

## 🚀 Features

### 🧠 Structured Prompt Architecture

DraftPilot uses structured prompts to guide the AI as a specialized copywriter based on user-defined constraints.

**Content Types:**

* Blog Posts
* Emails
* LinkedIn Posts
* Instagram Captions
* Product Descriptions
* Marketing Copy

**Tones:**

* Professional
* Friendly
* Persuasive
* Casual
* Technical
* Creative

**Customization:**

* Output Length
* Target Language
* Content Type
* Writing Tone

**Supported Languages:**

* English
* Persian
* Spanish
* French
* German

### 💾 Persistent Storage

Generated content is automatically stored in a PostgreSQL database.

Users can preserve their generated content instead of losing it after the application session ends.

### 📚 Content Archive

The **My Content** dashboard allows users to:

* Browse previous generations
* Copy generated content
* Delete saved content
* Review their content history

### 🛡️ Resilient API

DraftPilot includes:

* Automatic retry mechanisms for temporary AI service failures
* Daily IP-based rate limiting
* Input validation through Pydantic
* Backend error handling

---

## 🏗️ Architecture

DraftPilot uses a separated frontend/backend architecture:

```text
                User
                  │
                  ▼
        ┌──────────────────┐
        │    Streamlit     │
        │    Frontend      │
        └────────┬─────────┘
                 │
              HTTP API
                 │
                 ▼
        ┌──────────────────┐
        │     FastAPI      │
        │     Backend      │
        └────────┬─────────┘
                 │
        ┌────────┴─────────┐
        │                  │
        ▼                  ▼
 ┌──────────────┐   ┌──────────────┐
 │ Google Gemini│   │ PostgreSQL   │
 │     API      │   │   Database   │
 └──────────────┘   └──────────────┘
```

The Streamlit frontend is responsible for the user interface, while FastAPI handles API requests, validation, business logic, AI communication, rate limiting, and database operations.

---

## 🛠️ Tech Stack

### Backend

* Python 3.13
* FastAPI
* Uvicorn
* Pydantic

### Frontend

* Streamlit
* Requests

### Database

* PostgreSQL

### ORM & Database Driver

* SQLAlchemy
* `psycopg` v3

### AI

* Google Gemini API
* `google-genai`

---

## ⚙️ Local Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/iamhoss14/DRAFT-PILOT.git
cd DRAFT-PILOT
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

Install the project dependencies:

```bash
pip install fastapi uvicorn pydantic streamlit google-genai sqlalchemy "psycopg[binary]" python-dotenv requests
```

If the project contains a `requirements.txt`, you can instead use:

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Make sure PostgreSQL is installed and running.

Create the database:

```bash
sudo -u postgres psql -c "CREATE DATABASE draftpilot;"
```

If you need to configure a PostgreSQL password for local development:

```bash
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

> **Note:** The commands above are intended for local development. Do not use simple default credentials in a production environment.

### 5. Environment Variables

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_actual_api_key_here
```

Never commit your `.env` file to GitHub.

Make sure `.gitignore` contains:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Running the Application

The backend and frontend need to run simultaneously in two terminal windows.

### Terminal 1: FastAPI Backend

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

The FastAPI server will run at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Terminal 2: Streamlit Frontend

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the frontend:

```bash
streamlit run app/ui.py
```

The Streamlit application will normally be available at:

```text
http://localhost:8501
```

---

## 🗺️ Roadmap

### Phase 1: Core AI Integration

* [x] FastAPI backend
* [x] Streamlit frontend
* [x] Gemini API integration
* [x] Basic content generation
* [x] API error handling

### Phase 2: Prompt Architecture

* [x] Structured prompt system
* [x] Multiple content types
* [x] Multiple writing tones
* [x] Language selection
* [x] Output length control
* [x] Specialized content generation

### Phase 3: Persistent Storage

* [x] PostgreSQL integration
* [x] SQLAlchemy integration
* [x] Persistent content storage
* [x] Content history
* [x] My Content dashboard
* [x] Delete generated content

### Phase 4: Authentication

* [ ] User registration
* [ ] User login
* [ ] Password hashing
* [ ] JWT authentication
* [ ] Protected API endpoints
* [ ] User-isolated content
* [ ] User-specific workspaces

### Phase 5: SaaS Features

* [ ] User usage tracking
* [ ] Credit system
* [ ] Free plan
* [ ] Pro plan
* [ ] Subscription management
* [ ] Payment integration
* [ ] Payment webhooks

### Phase 6: Production Engineering

* [ ] Automated testing
* [ ] Docker
* [ ] CI/CD
* [ ] Production deployment
* [ ] Application logging
* [ ] Monitoring
* [ ] Health checks
* [ ] Production database configuration

### Phase 7: AI Engineering

* [ ] Prompt versioning
* [ ] Token usage tracking
* [ ] AI cost tracking
* [ ] Generation latency tracking
* [ ] Prompt evaluation
* [ ] Output quality evaluation
* [ ] Model comparison

---

## 📈 Project Vision

The long-term goal of DraftPilot is to evolve from an AI content generation application into a complete SaaS platform.

```text
MVP
 │
 ├── AI Generation
 ├── Prompt Architecture
 └── Streamlit UI
        │
        ▼
Persistent Application
 │
 ├── PostgreSQL
 ├── Content History
 └── Data Management
        │
        ▼
Multi-User SaaS
 │
 ├── Authentication
 ├── User Workspaces
 ├── Usage Tracking
 └── Subscription Plans
        │
        ▼
Production SaaS
 │
 ├── Payments
 ├── Docker
 ├── CI/CD
 ├── Monitoring
 └── Deployment
```

---

## 👨‍💻 Author

**Amirhossein Afzali**

GitHub: [@iamhoss14](https://github.com/iamhoss14)

---

## 📄 License

This project is currently developed for educational, portfolio, and product-development purposes.

---

## 🔄 Git Workflow

After updating the README:

```bash
git add README.md
git commit -m "Update README with Phase 2 and Phase 3 features"
git push origin main
```

Check the repository status with:

```bash
git status
```

A clean working tree should show:

```text
nothing to commit, working tree clean
```
