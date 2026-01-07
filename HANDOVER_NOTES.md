# 🚀 Deployment Handover Notes: Agno WorkSphere

This document provides critical technical information for the deployment and DevOps team to ensure a smooth transition to testing and production servers.

## 🏗️ Architecture Overview

- **Frontend**: React (SPA) - Statically served via Nginx, Apache, or S3.
- **Backend**: FastAPI (Python) - High-performance ASGI runner.
- **Protocol**: REST API + WebSockets for real-time updates.

---

## 🛠️ Infrastructure Requirements

- **PostgreSQL**: Primary DB (requires `asyncpg` compatibility).
- **Redis**: Caching and WebSocket session management.
- **Node.js 18+**: For frontend build phase only.
- **Python 3.8+**: Backend runtime.

---

## 🔑 High-Priority Configuration

### Backend (`.env`)

| Variable          | Importance   | Description                                |
| :---------------- | :----------- | :----------------------------------------- |
| `DATABASE_URL`    | **CRITICAL** | Must use `postgresql+asyncpg://` prefix.   |
| `ALLOWED_ORIGINS` | **CRITICAL** | Must match the exact Frontend hosting URL. |
| `JWT_SECRET`      | **Security** | 64-character random string for production. |
| `OPENAI_API_KEY`  | **Feature**  | Required for AI Summaries and Insights.    |

### Frontend (`.env`)

- `REACT_APP_API_URL`: Backend API endpoint URL.
- `REACT_APP_USE_REAL_BACKEND`: Set to `true`.

---

## 🚀 Deployment Sequence

1. **Database Migration**:
   ```bash
   alembic upgrade head
   ```
2. **Backend Startup**:
   ```bash
   python run_production.py
   ```
3. **Frontend Build**:
   ```bash
   npm install && npm run build
   ```

---

## 🛡️ Security & Networking

> [!IMPORTANT] > **CORS Configuration**: If you see `CORS Header Missing` errors, double-check that `ALLOWED_ORIGINS` in the backend `.env` perfectly matches the frontend URL (including `https://` and no trailing slash).

- **Port 8000**: Default Backend port.
- **Statics**: Serve the `FE/build` directory as static content.

---

## 🔗 External Dependencies

- **OpenAI API**: Powering the project status reporting.
- **Google Calendar**: (Experimental) Enable via `.env` for meeting syncing.

---

_For support, refer to the root [README.md](file:///d:/PM/fixing%20V3/README.md) or the [Deployment Checklist](file:///C:/Users/Ramprasath/.gemini/antigravity/brain/3299d407-8f99-4177-a952-82e90aa87d20/deployment_checklist.md)._
