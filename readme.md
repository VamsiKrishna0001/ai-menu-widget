# AI-Powered Menu Intelligence Widget

A full-stack application (React frontend + FastAPI backend) for generating short, catchy food item descriptions and upsell suggestions using AI.

---
## 🚀 Project Start (Quickstart Guide)

### Prerequisites
- **Node.js** v14+ and npm (for frontend)
- **Python** 3.8+ and pip (for backend)

## Project Structure
```
ai-menu-widget/
├── frontend/     # React app (UI)
├── backend/      # FastAPI app (API + AI integration)
├── .gitignore
└── README.md
```

---

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

### Environments Variables and Swagger Docs
- Add .env file add OPENAI_API_KEY

- Backend runs at 👉 http://localhost:8000
- Interactive docs 👉 http://localhost:8000/docs

```bash
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
- **Cursor AI (local dev integration)** – Assisted in writing and refining code & backend integration

---


## Prompt Design

The AI prompt was carefully designed to ensure consistent, marketing-ready menu text that matches how professional restaurants describe their dishes.

### Goals
1. **Generate a short, catchy description** (max 30 words) that sounds like a real menu.  
   - Engaging and food-friendly tone  
   - Sensory language (taste, smell, texture)  
   - Style inspired by professional menus (“crispy, juicy, tender, spicy”)  
   - Highlight premium ingredients and preparation methods  

2. **Suggest one upsell item** (side, drink, or dessert) that pairs naturally with the main dish.  
   - Keep it short, fun, and appealing  
   - Encourage customers to enhance their meal with an add-on  

### Iterations
- **Initial version**:  
  Prompted the model with `"Generate a description and upsell for {food_name}"`.  
  → Results were inconsistent (too long, sometimes multiple upsells, lacked style).

- **Second version**:  
  Added explicit formatting instructions (`DESCRIPTION:` and `UPSELL:`).  
  → More structured, but still sometimes exceeded 30 words.

- **Final version (system prompt used):**  
  ```text
  You are a professional AI food menu assistant and restaurant marketing expert. 
  Generate compelling descriptions and upsell messages for food items.
  Your Tasks:
  1. Generate a SHORT, catchy description (max 30 words).
     - Use engaging, food-friendly language.
     - Use sensory language (taste, smell, texture).
     - Style should be similar to professional menus (crispy, juicy, tender, spicy, etc.).
     - Do NOT exceed 30 words.
     - Include premium ingredients and preparation methods.
  2. Suggest ONE upsell item (a side, drink, or dessert that pairs well).
     - Suggest pairings or enhancements.
     - Keep it short, fun, and appealing.
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

## Future Enhancements

- Real DB integration (Postgres/MongoDB + Redis for cache)
- Auth + user history
- POS system integration hooks
- Multi-language support
- Deployment with Docker + Kubernetes

---
