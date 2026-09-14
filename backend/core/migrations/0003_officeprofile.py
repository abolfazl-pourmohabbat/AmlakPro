from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('core','0002_token')]
    operations = [migrations.CreateModel(name='OfficeProfile', fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('name', models.CharField(default='دفتر املاک', max_length=160)), ('phone', models.CharField(blank=True,max_length=30)),
        ('mobile', models.CharField(blank=True,max_length=30)), ('address', models.CharField(blank=True,max_length=300)),
        ('city', models.CharField(blank=True,max_length=80)), ('description', models.TextField(blank=True)),
        ('updated_at', models.DateTimeField(auto_now=True)),
    ], options={'verbose_name':'اطلاعات دفتر','verbose_name_plural':'اطلاعات دفتر'})]
