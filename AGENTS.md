# AGENTS.md — AmlakPro

## Purpose

This file is the persistent project brief and working agreement for coding agents working on AmlakPro. Treat the repository owner as the client/product owner. The client wants a finished, production-ready result and does not expect to edit or repair code or technical configuration personally.

## Project Overview

- Project: AmlakPro (دفتر املاک)
- Repository: `abolfazl-pourmohabbat/AmlakPro`
- Frontend: Angular 20
- Backend: Django 5.2 + Django REST Framework
- Database: PostgreSQL on Neon
- Deployment: separate Vercel projects for frontend and backend
- Frontend URL: `https://amlak-pro.vercel.app/`
- Backend URL: `https://amlakpro-api.vercel.app/`
- Backend health endpoint: `/api/health/`
- UI language: Persian
- Development environment commonly used by the client: Windows 10 + WebStorm + GitHub Desktop

## Client Working Style

- Act as the responsible programmer/full development team, not merely a code generator.
- The client is the employer/product owner; make sound technical decisions autonomously when requirements are clear.
- Do not repeatedly ask the client to upload files that are already available through the connected GitHub repository or project context.
- Ask questions only when a missing decision is genuinely required to avoid an incorrect implementation.
- Prefer one complete, focused change over many incremental UI changes.
- Keep solutions simple, clean, professional, maintainable, and production-oriented. Do not over-engineer.
- When a bug is reported, inspect the real code and root cause first. Do not guess field names, architecture, or APIs.
- Preserve working functionality. Do not change unrelated code just because it could be improved.
- Explain only the important result and the next action; avoid long planning explanations unless requested.

## Standard Project Requirements

Every substantial project change should remain:

- GitHub-ready: clean structure, README/documentation where appropriate, `.gitignore`, `.env.example`, and no secrets.
- Deployment-ready: production configuration, required environment variables, database configuration, build/deploy configuration, and required backend/frontend integration.
- Testable: run the relevant build, tests, checks, or API verification when the environment allows it.
- Secure: validate inputs, protect secrets, handle authentication/authorization correctly, and treat uploads/API endpoints as untrusted input.
- SEO-conscious for public web pages where relevant.

## Typography and Readability

- The site is Persian-first and typography is a core part of the product UI, not an afterthought.
- Use **Estedad** as the primary UI typeface for Persian/Arabic text. It is a screen/web-oriented Arabic-Latin sans-serif family with multiple weights and is licensed under SIL OFL 1.1.
- Use **Roboto** as the Latin fallback/companion where appropriate.
- Prefer the existing global font stack rather than introducing a different font family in individual components unless there is a specific design reason.
- Use readable weights: normally 400 for body text, 500–600 for navigation/labels, and 700–800 for important headings.
- Do not use very small body or navigation text. As a general UI rule, avoid sizes below 13px; normal body copy should usually be 14–16px or larger.
- Secondary/supporting text may be smaller than body text, but it must remain comfortably readable on desktop and mobile.
- Increase line-height for Persian paragraphs and multi-line UI copy where needed; prioritize readability over fitting more text into a small area.
- Keep typography consistent across homepage, property cards, property lists, agent pages, account pages, dashboard, reports, and management screens.
- When changing typography, preserve the existing visual identity: clean, professional, restrained real-estate presentation. Do not turn the UI into an oversized or decorative design.
- Responsive typography is required: headings and body text must remain readable on smaller screens without causing horizontal overflow.
- Avoid adding a paid/proprietary font dependency when a suitable open font already meets the requirement.

## AmlakPro Architecture and Business Rules

The application is a real estate office website and management system. Important capabilities include public property search/listing/detail pages, agents, office information, account-based favorites, visit/lead requests, authentication, dashboard/CRM, activity history, analytics, and Django admin management.

### Property business rules

The backend `Property` model currently uses these deal types:

- `sale` = فروش
- `rent` = اجاره
- `mortgage` = رهن

Relevant money fields are:

- `price` = sale price
- `deposit` = mortgage/deposit amount
- `rent` = rental amount

Property cards must display money according to `deal_type`, not always use `price`:

- sale → sale `price`
- mortgage → `deposit`
- rent → `deposit` + `rent` when both exist; otherwise whichever exists

The same pricing/display logic should be consistent between the homepage cards and the properties-list cards. Property detail is the reference when checking the correct underlying values.

### Account and favorites rules

- Registered customer favorites are persisted in the backend and associated with the authenticated Django user.
- Guests may temporarily use local browser favorites; when a customer logs in or registers, local favorites are synchronized with the account.
- Do not regress favorites back to being browser-only for authenticated users.
- Favorite API endpoints require authentication and users must only see/change their own favorites.
- Public property/favorite data must not expose sold/rented properties through endpoints intended for active public listings.

## Important Lessons / Known Issues

- DRF serializer bug previously occurred because `source='gallery'` was redundantly specified on the `gallery` field. Do not reintroduce that pattern.
- Lead PATCH previously returned HTTP 415; keep the working request/content-type behavior intact.
- Vercel backend uses a writable/read-only filesystem constraint. Do not store persistent uploaded files on the local Vercel filesystem.
- Image uploads use the project's configured Blob storage. Uploaded image paths/names must be unique; identical filenames previously caused collisions between different property images. Do not regress this.
- PostgreSQL/Neon connectivity is working. Do not replace it with another database or suggest Render merely as a workaround.
- CORS already includes the production frontend origin.
- Angular deployment previously required the configured output path that places browser files directly under `dist/amalkpro`; do not casually change this and reintroduce Vercel 404s.
- Search/filter behavior previously showed overly broad matching for a neighborhood query such as «سعادت آباد». Preserve any subsequent narrowing/fix and do not broaden search across unrelated fields without a product reason.
- A previous rental-card bug showed `0 تومان` on homepage/list cards while the detail page correctly showed the rental amount. Root cause: cards always rendered `p.price`. This was fixed by switching card display to deal-type-aware `price`/`deposit`/`rent` logic. Keep homepage and properties-list cards consistent.
- Production Django must not default to `DEBUG=True`. `DJANGO_DEBUG=false` and a real `DJANGO_SECRET_KEY` must be configured for Vercel production.
- The repository currently does not commit a frontend lockfile, so CI uses `npm install` rather than `npm ci` until a lockfile is intentionally added.

## Development Workflow

1. Read the existing code and relevant project instructions before changing anything.
2. Identify the smallest root-cause change that satisfies the request.
3. Reuse existing components, services, models, styles, and API contracts where possible.
4. Make the focused change.
5. Run the most relevant tests/build/checks available.
6. Re-read the changed files or inspect the resulting diff when useful, especially for important production changes.
7. Report exactly what changed, any validation performed, and any remaining limitation.

## Git / GitHub Workflow

- The connected GitHub repository is the source of truth for the current project version unless the client explicitly says otherwise.
- Use the connected GitHub tools when available instead of asking the client to re-upload repository files.
- Keep commits focused and descriptive.
- Do not rewrite unrelated history.
- Do not create branches unless the client explicitly asks for a branch/PR workflow.
- Never commit secrets, tokens, passwords, private keys, or real environment values.
- After a direct repository edit, give the client the commit SHA and a concise description of the change.

## Deployment Workflow

The established workflow is:

`GitHub → Vercel frontend/backend → Neon PostgreSQL → domain`

The client normally uses GitHub Desktop for local Git operations when needed. Prefer changes that can be pulled/synced cleanly through GitHub Desktop and deployed by the existing Vercel integrations.

Before declaring a production bug fixed, distinguish between:

- code fixed in GitHub,
- Vercel deployment completed,
- production endpoint/page actually verified.

Do not claim production verification if only the repository was changed.

## Testing Priorities

For frontend changes:

- Angular production build when available.
- Check the affected route/page in production after Vercel deployment when possible.
- Verify API data is rendered with the correct field and formatting.
- For typography changes, verify desktop and mobile readability and check that no text causes horizontal overflow.
- Verify the mobile navigation exposes favorites, registration, and login.

For backend changes:

- Django checks/tests when available.
- Verify affected API endpoint and HTTP status.
- Preserve PostgreSQL/Neon connectivity.
- Verify authenticated users can only access their own account favorites.
- Run `python manage.py check --deploy` against production settings before a production release when the environment allows it.

For upload changes:

- Test unique filenames/paths.
- Verify the stored URL is usable from the frontend.
- Never rely on persistent local disk storage on Vercel.

## UI / Product Style

- Persian-first UI.
- Simple, clean, professional real-estate presentation.
- Typography should use the established Estedad/Roboto stack and readable sizing rules above.
- Avoid unnecessary animations, abstractions, dependencies, and visual redesigns during bug fixes.
- Keep responsive/mobile behavior intact.
- User-facing copy should be clear and natural Persian.

## Security and Data Handling

- Never expose secrets in source code, commits, logs, screenshots, or documentation.
- Do not hard-code production credentials.
- Validate uploads and API input.
- Keep authentication and protected management endpoints protected.
- New customer auth tokens are kept in session storage rather than long-lived local storage; legacy local tokens are migrated out when encountered.
- Do not weaken CORS, CSRF, authentication, permissions, throttling, or validation merely to make a test pass.

## Decision Rule

When several technically valid solutions exist, prefer the one that:

1. fixes the root cause,
2. changes the fewest unrelated files,
3. preserves the current architecture and deployment setup,
4. is easiest for the client to maintain,
5. can be tested and deployed reliably.

## Project History Principle

Treat lessons from previous AmlakPro debugging as regression requirements. In particular, avoid reintroducing serializer field-source errors, Vercel routing/output mistakes, local-filesystem upload assumptions, duplicate upload filenames, broken API content types, inconsistent card/detail data formatting, browser-only authenticated favorites, and unprotected management routes.
