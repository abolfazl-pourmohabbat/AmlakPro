from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('core','0006_expand_site_settings')]
    operations = [
        migrations.AddField(model_name='sitesettings',name='contact_office_name_label',field=models.CharField(default='نام دفتر',max_length=80)),
        migrations.AddField(model_name='sitesettings',name='contact_city_label',field=models.CharField(default='شهر',max_length=80)),
        migrations.AddField(model_name='sitesettings',name='contact_description_label',field=models.CharField(default='معرفی دفتر',max_length=80)),
    ]
