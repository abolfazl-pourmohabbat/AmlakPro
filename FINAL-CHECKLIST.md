# AmlakPro — Final Checklist

## Local
1. `cd backend && python manage.py migrate`
2. `python manage.py test`
3. `cd ../frontend && npm install && npm run build`

## Production
1. Copy `backend/.env.example` to `backend/.env` and replace all placeholders.
2. Set `DJANGO_DEBUG=false`.
3. Set real `DJANGO_ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`.
4. Use a strong unique PostgreSQL password.
5. Run `docker compose up --build`.
6. Run `docker compose exec backend python manage.py check --deploy`.
7. Put the stack behind HTTPS.
8. Configure database and media backups.

## Important
Never commit `backend/.env`, real secrets, production database credentials, `media/`, `staticfiles/`, `dist/`, or `node_modules/`.
