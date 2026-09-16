# AmlakPro — Lead Status Fix

این patch فقط باگ ذخیره‌نشدن وضعیت Lead را اصلاح می‌کند.

علت:
`status` در `LeadSerializer` به اشتباه `read_only` بود؛ بنابراین PATCH/PUT داشبورد وضعیت را دریافت می‌کرد اما DRF آن را برای ذخیره وارد `validated_data` نمی‌کرد.

اصلاح:
`status` از `read_only_fields` حذف شده و حالا تغییر وضعیت توسط کاربر staff از طریق endpoint موجود `/api/leads/<id>/` قابل ذخیره است.

فایل جایگزین:
`backend/core/serializers.py`
