# AI-Powered Menu Intelligence Widget

A full-stack application (React frontend + FastAPI backend) for generating short, catchy food item descriptions and upsell suggestions using AI.

---
## 🚀 Project Start (Quickstart Guide)

### Prerequisites
- **Node.js** v14+ and npm (for frontend)
- **Python** 3.8+ and pip (for backend)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/ai-menu-widget.git
cd ai-menu-widget
cd backend
python -m venv venv          # create virtual environment
source venv/bin/activate     # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Add .env file add OPENAI_API_KEY
Backend runs at 👉 http://localhost:8000
Interactive docs 👉 http://localhost:8000/docs
```

```
cd frontend
npm install
npm start
```

## Tools Used

### Frontend
- **React 18.2.0** – UI framework
- **React-toastify** – Notifications
- **CSS3** – Modern styling with gradients, transitions, backdrop-filter
- **Create React App** – Project scaffolding

### Backend
- **FastAPI 0.104.1** – Modern Python API framework
- **Pydantic 2.5.0** – Data validation and sanitization
- **Uvicorn** – ASGI server
- **JSON files** – Lightweight persistence for history and cache

### AI Tools
- **OpenAI GPT-3.5 / GPT-4 (planned)** – For generating menu descriptions and upsell suggestions  
- **Cursor AI (local dev integration)** – Assisted in writing and refining prompts & backend integration

---

## Prompt Design

The AI prompt was carefully designed to achieve **two goals**:
1. **Short, catchy descriptions** (max 30 words, menu-style tone: "crispy, juicy, tender").  
2. **One upsell suggestion** (a side, drink, or dessert that pairs naturally).

### Iterations:
- **First attempt:** Simple prompt `"Generate a description and upsell for Paneer Tikka Pizza"` → results were inconsistent, sometimes too long.  
- **Second iteration:** Added explicit **format requirement** (`DESCRIPTION: ... / UPSELL: ...`) → more structured, but still verbose.  
- **Final iteration:**  
  - Limited to **30 words max**.  
  - Added **tone guidance** (“engaging, food-friendly, like a menu”).  
  - Forced **JSON output** for reliable backend parsing.  

This ensures responses are **short, styled like real menus, and machine-parseable**.

---

## Time Taken & Tradeoffs

- **Total Time**: ~3–6 hours  
  - Backend setup & validation: ~1 hrs  
  - Frontend UI with toggles: ~2 hrs  
  - Prompt engineering & testing: ~1 hrs  
  - Caching & persistence: ~30 min 
  - Documentation & cleanup: ~ 30 min  

### Tradeoffs / Assumptions:
- **Database**: Not used (JSON storage chosen for simplicity & easy grading). A real POS would use PostgreSQL/Redis.  
- **Rate limiting**: Implemented basic pseudo-code. In production, would use `slowapi` or API gateway.  
- **AI quota**: Mock responses fallback used since OpenAI API quota may run out during testing.  
- **Model toggle**: Currently limited to GPT-3.5 (tested) with placeholder toggle for GPT-4 (not available in free quota).  
- **Integration**: API are integration to frontend, using the api we get upsell and description from openAI response, Description can be copied from the frontend which is generated from openAI and can be used as well.

---

## Project Structure
ai-menu-widget/
├── frontend/     # React app (UI)
├── backend/      # FastAPI app (API + AI integration)
├── .gitignore
└── README.md

---

## Future Enhancements

- Real DB integration (Postgres/MongoDB + Redis for cache)
- Auth + user history
- POS system integration hooks
- Multi-language support
- Deployment with Docker + Kubernetes

---