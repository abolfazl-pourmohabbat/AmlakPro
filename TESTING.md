# تست پروژه

## Backend

از ریشه پروژه:

```bash
python backend/manage.py test
```

تست‌ها موارد اصلی API را پوشش می‌دهند: دسترسی عمومی ملک، احراز هویت، سطح دسترسی Staff، Lead، پیگیری و Dashboard.

## Frontend

```bash
cd frontend
npm install
npm test
npm run build
```

تست فعلی Frontend رفتار علاقه‌مندی‌ها را بررسی می‌کند. برای HTTP هم در ادامه می‌توان تست‌های سرویس API را با `provideHttpClientTesting()` اضافه کرد.

## CI

فایل `.github/workflows/ci.yml` تست Backend، تست Frontend و Production build را روی push و pull request اجرا می‌کند.
