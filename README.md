# FactOrNot 🔍

An enterprise-grade AI-powered news and fact-checking web application designed to instantly verify text claims and analyze image uploads with multi-source validation.

---

## 🚀 Live Demo & Architecture
* **Frontend:** Deployed live on Vercel
* **Backend:** Deployed live on Render (`https://fact-or-not-backend.onrender.com`)
* **Core Engine:** FastAPI, Google GenAI SDK, Tavily Search API, and Pillow.

---

## ✨ Key Features
* **Multi-Modal Verification:** Support for checking both written text claims and uploaded image/screenshot evidence.
* **Dynamic Theme Shifts:** Interface dynamically transitions colors based on the verification verdict:
  * 🔴 **Crimson/Red** for False/Misleading claims.
  * 🟢 **Emerald/Green** for True/Verified claims.
  * 🔵 **Blue** for Neutral or Unverified claims.
* **macOS-Inspired Frosted Glass UI:** Sleek, modern dark-mode aesthetic with smooth pill buttons and hover lift effects.
* **Clear Reset Flow:** Fast, intuitive "Check Another Claim" cycle.

---

## 🛠️ Tech Stack

### Backend (`main.py`)
* **Framework:** FastAPI (Python 3.11+)
* **AI & Search:** Google GenAI SDK & Tavily Search API
* **Image Processing:** Pillow (`PIL`)
* **Server:** Uvicorn

### Frontend (`frontend/`)
* **Framework:** Next.js / React
* **Styling:** Pure CSS & Inline React Styles

---

## 📂 Project Structure

```text
fact-or-not/
├── main.py              # FastAPI backend entrypoint
├── requirements.txt     # Python package dependencies
├── runtime.txt          # Python version configuration (3.11.11)
├── Dockerfile           # Container configuration
├── README.md            # Project documentation
└── frontend/            # Next.js frontend application
    └── app/
        └── page.tsx     # Main UI and API integration logic

```

---

## ⚙️ Local Development Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/DeepakRawatSftwrDvlpr7/fact-or-not.git](https://github.com/DeepakRawatSftwrDvlpr7/fact-or-not.git)
cd fact-or-not

```

### 2. Configure Environment Variables

Create a `.env` file in the root directory and add your API keys:

```env
GEMINI_API_KEY=your_google_genai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

```

### 3. Run the Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

```

### 4. Run the Frontend

Navigate to the frontend directory, install dependencies, and start the development server:

```bash
cd frontend
npm install
npm run dev

```

---

## 📦 Deployment & Configuration

* **Backend (Render):**
* Root Directory: *Leave blank*
* Build Command: `pip install --only-binary=:all: -r requirements.txt`
* Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`


* **Frontend (Vercel):** Automatically builds and serves the Next.js static/dynamic pages linked to the live backend API endpoint (`https://fact-or-not-backend.onrender.com/api/verify`).

---

## 👨‍💻 Developer Attribution

Created and maintained by **Deepak Rawat** (Branded under **FactOrNot** with the **FON** logo).

```

```
