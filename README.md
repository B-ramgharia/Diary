# Diary. - Secure & Premium Personal Journal

A modern, full-stack diary application built with Next.js 15 and Flask. Capture your thoughts in a beautifully designed, secure space.

## Features
- **Authentication**: Secure JWT-based login and registration.
- **Personal Dashboard**: Manage your journals with a premium Polaroid-style interface.
- **Full CRUD**: Create, Read, Update, and Delete journal entries.
- **Search & Filter**: Find your memories instantly.
- **Premium UI**: Glassmorphism design with sleek animations using `framer-motion`.
- **Responsive**: Fully optimized for mobile and desktop.

## Tech Stack
- **Frontend**: Next.js (React), Tailwind CSS, Framer Motion, Lucide Icons.
- **Backend**: Flask, SQLAlchemy (SQLite), Flask-Bcrypt, Flask-JWT-Extended.
- **Database**: SQLite (Development). Easily migratable to PostgreSQL/MySQL.

## Scalability & Production Considerations
To scale this application for production, the following steps are recommended:

1. **Database Migration**:
   - Replace SQLite with a robust RDBMS like **PostgreSQL** or **managed MongoDB**.
   - Use specialized services like Supabase or MongoDB Atlas for high availability.

2. **State Management**:
   - While `AuthContext` works for small apps, use **React Query (TanStack Query)** for fetching and caching entries to improve performance and reduce server load.

3. **Media Storage**:
   - Instead of static images, allow users to upload covers via **AWS S3** or **Cloudinary**.

4. **Security**:
   - Move all secrets to environmental variables (`.env`).
   - Implement **refresh tokens** for better security.
   - Use HTTPS and add rate limiting to the API.

5. **Deployment**:
   - Frontend: Vercel / Netlify.
   - Backend: Render / Railway / AWS App Runner.
   - Dockerize the application for consistent environments.

## 🚀 Deployment (Recommended: Render)

Since this is a Flask app with a database, it cannot be hosted on GitHub Pages. We recommend using **Render** for free hosting:

1. **Create a Render Account**: Sign up at [render.com](https://render.com).
2. **New Web Service**: Select "New +" > "Web Service".
3. **Connect GitHub**: Connect your repository `https://github.com/B-ramgharia/Diary`.
4. **Configure Settings**:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. **Add Environment Variables** (Optional but recommended):
   - `SECRET_KEY`: A random secure string.
6. **Deploy**: Click "Create Web Service". Your app will be live in a few minutes!

> [!NOTE]
> Render's free tier spins down after inactivity, so the first load might take a few seconds.

---

## Local Setup
1. **Repository Structure**:
   - Root directory: Contains `app.py`, `templates/`, `static/`, and `diary.db`.
2. **Setup**:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
