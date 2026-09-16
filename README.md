# AmlakPro

<p align="center">
  <strong>سامانه حرفه‌ای مدیریت و معرفی املاک</strong>
</p>

<p align="center">
  وب‌سایت مدرن املاک با جست‌وجوی ملک، مدیریت فایل‌ها، CRM، مدیریت مشاوران و ثبت درخواست بازدید
</p>

<p align="center">
  <a href="https://amlak-pro.vercel.app/">مشاهده نسخه آنلاین</a>
  ·
  <a href="https://amlakpro-api.vercel.app/api/health/">Backend Health</a>
</p>

---

## معرفی

**AmlakPro** یک پلتفرم وب برای دفاتر املاک است که دو بخش اصلی دارد:

- **وب‌سایت عمومی** برای نمایش و جست‌وجوی املاک و ارتباط مشتری با دفتر
- **پنل مدیریت و CRM** برای مدیریت املاک، مشاوران، سرنخ‌های فروش و درخواست‌های مشتریان

هدف پروژه ارائه یک تجربه ساده، سریع و حرفه‌ای برای مشتریان و در عین حال فراهم‌کردن ابزارهای کاربردی برای مدیریت روزانه یک دفتر املاک است.

## قابلیت‌ها

### وب‌سایت عمومی

- نمایش املاک و املاک ویژه
- جست‌وجوی ملک بر اساس عنوان، شهر و محله
- فیلتر بر اساس نوع معامله و نوع ملک
- مرتب‌سازی و صفحه‌بندی نتایج
- صفحه اختصاصی هر ملک
- نمایش تصاویر و گالری ملک
- نمایش اطلاعات مشاور
- ثبت درخواست بازدید و تماس
- علاقه‌مندی‌ها
- معرفی دفتر و اطلاعات تماس
- طراحی Responsive برای موبایل، تبلت و دسکتاپ
- صفحات خطای کاربردی و مسیرهای کاربرپسند

### مدیریت و CRM

- ورود امن کاربران مدیریتی
- مدیریت املاک
- ایجاد، ویرایش و حذف ملک
- مدیریت تصاویر ملک
- مدیریت مشاوران
- مدیریت سرنخ‌ها (Leads)
- تغییر وضعیت سرنخ‌ها
- ثبت فعالیت و تاریخچه پیگیری
- تعیین تاریخ پیگیری بعدی
- داشبورد مدیریتی
- آمار و Analytics
- مدیریت اطلاعات دفتر
- Django Admin

### منطق معاملات

AmlakPro از سه نوع معامله پشتیبانی می‌کند:

| نوع معامله | اطلاعات مالی نمایش‌داده‌شده |
|---|---|
| فروش | قیمت فروش |
| رهن | مبلغ رهن |
| اجاره | مبلغ رهن و مبلغ اجاره، در صورت وجود |

کارت‌های صفحه اصلی و صفحه املاک، مبلغ را بر اساس نوع معامله نمایش می‌دهند تا اطلاعات مالی هر ملک به شکل صحیح ارائه شود.

## تکنولوژی‌ها

### Frontend

- Angular 20
- TypeScript
- HTML / CSS
- Angular Router
- Angular Forms
- Angular HttpClient
- Angular Optimized Images

### Backend

- Python
- Django 5.2
- Django REST Framework
- django-filter
- Token Authentication

### Database & Infrastructure

- PostgreSQL
- Neon PostgreSQL
- Vercel
- Vercel Blob برای فایل‌ها و تصاویر آپلودی

## معماری پروژه

```text
AmlakPro/
├── frontend/          # Angular application
│   └── src/app/
├── backend/           # Django + Django REST Framework
│   ├── config/
│   └── core/
├── AGENTS.md          # دستورالعمل‌های پایدار پروژه برای توسعه
├── README.md
└── ...
```

Frontend و Backend به‌صورت جداگانه روی Vercel Deploy می‌شوند و Backend به PostgreSQL روی Neon متصل است.

## آدرس‌های آنلاین

| بخش | آدرس |
|---|---|
| وب‌سایت | https://amlak-pro.vercel.app/ |
| Backend API | https://amlakpro-api.vercel.app/ |
| Health Check | https://amlakpro-api.vercel.app/api/health/ |
| Repository | https://github.com/abolfazl-pourmohabbat/AmlakPro |

## راه‌اندازی Frontend

وارد پوشه `frontend` شوید:

```bash
cd frontend
npm install
npm start
```

برای Build تولیدی:

```bash
npm run build
```

در محیط توسعه، Angular معمولاً روی آدرس زیر در دسترس است:

```text
http://localhost:4200
```

## راه‌اندازی Backend

وارد پوشه `backend` شوید:

```bash
cd backend
```

محیط مجازی Python را ایجاد و فعال کنید، سپس dependencyها را نصب کنید.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

سپس:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend توسعه‌ای روی آدرس زیر اجرا می‌شود:

```text
http://127.0.0.1:8000
```

## متغیرهای محیطی

اطلاعات حساس نباید داخل Git commit شوند. برای اجرای محلی، متغیرهای محیطی پروژه را مطابق فایل‌های نمونه و تنظیمات موجود در repository تنظیم کنید.

متغیرهای مهم Backend شامل مواردی مانند موارد زیر هستند:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DATABASE_URL=your-postgresql-url
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.com
BLOB_READ_WRITE_TOKEN=your-blob-token
```

**مقادیر واقعی Secret، Database URL و Token نباید در repository قرار بگیرند.**

## API

برخی endpointهای اصلی Backend:

```text
GET    /api/health/
GET    /api/properties/
GET    /api/properties/<slug>/
POST   /api/properties/
PATCH  /api/properties/<slug>/
DELETE /api/properties/<slug>/
GET    /api/agents/
GET    /api/office/
POST   /api/leads/
GET    /api/leads/manage/
PATCH  /api/leads/<id>/
GET    /api/dashboard/
GET    /api/analytics/
```

Endpointهای مدیریتی نیازمند احراز هویت و سطح دسترسی مناسب هستند.

## جست‌وجو و فیلتر املاک

پارامتر `q` برای جست‌وجوی متنی ملک استفاده می‌شود و عبارت واردشده را در **عنوان، شهر و محله** بررسی می‌کند.

نمونه:

```text
/api/properties/?q=سعادت%20آباد&public=1
```

فیلترهای اصلی نیز شامل موارد زیر هستند:

- نوع معامله
- نوع ملک
- شهر
- محله
- وضعیت
- تعداد خواب
- متراژ
- محدوده قیمت
- مرتب‌سازی

## تصاویر و فایل‌ها

تصاویر ملک از طریق سیستم ذخیره‌سازی پروژه مدیریت می‌شوند و در محیط Vercel نباید روی filesystem محلی به‌عنوان storage دائمی حساب شود.

برای تصاویر، نام و مسیر فایل باید یکتا باشد تا آپلود تصاویر با نام مشابه برای املاک مختلف باعث برخورد و overwrite نشود.

## امنیت

در محیط Production موارد زیر باید به‌درستی تنظیم شوند:

- Secretهای واقعی خارج از repository
- Authentication و Permission برای endpointهای مدیریتی
- CORS و CSRF مطابق دامنه‌های واقعی
- اعتبارسنجی داده‌های ورودی
- اعتبارسنجی فایل‌های آپلودی
- محدودسازی درخواست‌های حساس
- استفاده از HTTPS

برای repository عمومی، GitHub نیز فعال‌کردن قابلیت‌هایی مانند Dependabot alerts، secret scanning، push protection و code scanning را توصیه می‌کند. citeturn0search0

## توسعه و نگهداری

قبل از تغییرات مهم:

1. کد فعلی و معماری موجود بررسی شود.
2. علت اصلی مشکل مشخص شود.
3. کوچک‌ترین تغییر لازم اعمال شود.
4. قابلیت‌های سالم پروژه بدون دلیل تغییر نکنند.
5. Build و تست‌های مرتبط اجرا شوند.
6. تغییرات بررسی و سپس commit شوند.

فایل [`AGENTS.md`](./AGENTS.md) قوانین و تجربه‌های مهم پروژه را برای توسعه‌دهندگان و coding agentها نگه‌داری می‌کند.

## وضعیت پروژه

AmlakPro یک پروژه فعال و قابل استقرار است و توسعه آن بر اساس نیازهای واقعی دفتر املاک ادامه پیدا می‌کند.

---

## توسعه‌دهنده

**AmlakPro**

Repository: [abolfazl-pourmohabbat/AmlakPro](https://github.com/abolfazl-pourmohabbat/AmlakPro)

نسخه آنلاین: [amlak-pro.vercel.app](https://amlak-pro.vercel.app/)
