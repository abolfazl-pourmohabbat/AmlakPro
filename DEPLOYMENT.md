# AmlakPro Deployment Guide

## Recommended production layout

AmlakPro is a two-service application:

- `frontend/` — Angular application
- `backend/` — Django REST API + PostgreSQL

Keep the complete repository in GitHub. Deploy the frontend and backend as separate services when using platforms that are optimized for one runtime per project.

## GitHub

Create an empty repository and push the project root. Do not initialize the remote repository with another README or `.gitignore` because this repository already contains them.

Before the first push, confirm that these are **not** present:

- `backend/.env`
- real passwords or API keys
- `frontend/node_modules/`
- `frontend/dist/`
- local SQLite databases
- Django media uploads

## Vercel — Angular frontend

Import the GitHub repository into Vercel and set:

- **Root Directory:** `frontend`
- **Framework Preset:** Angular (auto-detect if offered)
- **Build Command:** `npm run build`
- **Output Directory:** use the directory reported by the Angular build if Vercel does not detect it automatically

Add the frontend API URL as an environment variable using the name expected by the Angular environment configuration in this project.

The Django API and PostgreSQL database are not hosted by this Vercel frontend deployment. Deploy them on a backend-capable host and point the Angular app to that API URL.

## Docker / VPS

For a single-server deployment, copy `backend/.env.example` to `backend/.env`, fill all production values, then run:

```bash
docker compose up --build -d
```

Before exposing the service publicly:

```bash
docker compose exec backend python manage.py check --deploy
```

Put the stack behind HTTPS and configure the real domain in Django's allowed hosts and CORS settings.

## Database and media backups

Back up both Docker volumes:

- `postgres_data`
- `media_data`

A database backup alone does not preserve uploaded property images.
