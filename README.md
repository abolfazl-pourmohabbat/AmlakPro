# AmlakPro — Lead Status PATCH Fix v2

علت خطای 415 در داشبورد این بود که `setStatus()` مقدار وضعیت را به صورت string خام (`contacted`) به PATCH می‌فرستاد.

اصلاح:
- ارسال وضعیت به شکل JSON: `{ status: 'contacted' }`
- endpoint همان `/api/leads/<id>/` باقی می‌ماند.
- Backend فعلی پروژه نیز باید شامل اصلاح `LeadSerializer` باشد که `status` را writable کرده است.

فایل:
`frontend/src/app/features/dashboard.component.ts`
