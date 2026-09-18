from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('core','0005_site_settings')]
    operations = [
        migrations.AddField(model_name='sitesettings',name='properties_eyebrow',field=models.CharField(default='املاک',max_length=100)),
        migrations.AddField(model_name='sitesettings',name='properties_title',field=models.CharField(default='گزینه مناسب بعدی شما',max_length=180)),
        migrations.AddField(model_name='sitesettings',name='properties_intro',field=models.TextField(default='جست‌وجو و فیلتر بین املاک موجود دفتر.')),
        migrations.AddField(model_name='sitesettings',name='properties_search_placeholder',field=models.CharField(default='شهر، محله یا نام ملک',max_length=180)),
        migrations.AddField(model_name='sitesettings',name='properties_deal_label',field=models.CharField(default='نوع معامله',max_length=80)),
        migrations.AddField(model_name='sitesettings',name='properties_type_label',field=models.CharField(default='نوع ملک',max_length=80)),
        migrations.AddField(model_name='sitesettings',name='properties_ordering_label',field=models.CharField(default='مرتب‌سازی',max_length=80)),
        migrations.AddField(model_name='sitesettings',name='properties_apply_button',field=models.CharField(default='اعمال فیلتر',max_length=80)),
        migrations.AddField(model_name='sitesettings',name='properties_clear_button',field=models.CharField(default='پاک کردن',max_length=80)),
        migrations.AddField(model_name='sitesettings',name='properties_prev_button',field=models.CharField(default='قبلی',max_length=60)),
        migrations.AddField(model_name='sitesettings',name='properties_next_button',field=models.CharField(default='بعدی',max_length=60)),
        migrations.AddField(model_name='sitesettings',name='properties_loading_text',field=models.CharField(default='در حال دریافت املاک...',max_length=160)),
        migrations.AddField(model_name='sitesettings',name='properties_error_text',field=models.CharField(default='دریافت فهرست املاک انجام نشد.',max_length=180)),
        migrations.AddField(model_name='sitesettings',name='properties_empty_text',field=models.CharField(default='ملکی مطابق جست‌وجوی شما پیدا نشد.',max_length=180)),
        migrations.AddField(model_name='sitesettings',name='properties_count_label',field=models.CharField(default='ملک',max_length=60)),
        migrations.AddField(model_name='sitesettings',name='agents_eyebrow',field=models.CharField(default='تیم ما',max_length=100)),
        migrations.AddField(model_name='sitesettings',name='agents_title',field=models.CharField(default='مشاورانی که کنار شما هستند',max_length=180)),
        migrations.AddField(model_name='sitesettings',name='agents_intro',field=models.TextField(default='تخصص محلی، پاسخ‌گویی و همراهی تا پایان معامله.')),
        migrations.AddField(model_name='sitesettings',name='agents_empty_text',field=models.CharField(default='هنوز مشاوری ثبت نشده است.',max_length=180)),
        migrations.AddField(model_name='sitesettings',name='agents_phone_label',field=models.CharField(default='تماس با مشاور',max_length=80)),
        migrations.AddField(model_name='sitesettings',name='about_button',field=models.CharField(default='مشاهده املاک',max_length=100)),
        migrations.AddField(model_name='sitesettings',name='footer_office_empty_text',field=models.CharField(default='اطلاعات دفتر در حال تکمیل است.',max_length=180)),
        migrations.AddField(model_name='sitesettings',name='whatsapp_url',field=models.URLField(blank=True)),
        migrations.AddField(model_name='sitesettings',name='instagram_label',field=models.CharField(default='اینستاگرام',max_length=60)),
        migrations.AddField(model_name='sitesettings',name='telegram_label',field=models.CharField(default='تلگرام',max_length=60)),
        migrations.AddField(model_name='sitesettings',name='whatsapp_label',field=models.CharField(default='واتساپ',max_length=60)),
    ]
