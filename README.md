# Submission Form App

This is a simple web application with:

- A frontend form for name, email, and phone number
- An automatically changing background color
- A Python backend API built with FastAPI
- MongoDB storage using an online MongoDB Atlas connection

## 1. Install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Configure MongoDB Atlas

1. Create a free cluster in MongoDB Atlas.
2. Create a database user.
3. Allow your IP in **Network Access**.
4. Copy `.env.example` to `.env`.
5. Replace `MONGODB_URI` with your Atlas connection string.

Example:

```env
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/codex_app?retryWrites=true&w=majority
MONGODB_DB=codex_app
MONGODB_COLLECTION=submissions
```

## 3. Run the app

```powershell
uvicorn app:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 4. What happens on submit

- The frontend sends the form data to `POST /api/submissions`
- The Python backend validates the data
- The backend stores the record in MongoDB
