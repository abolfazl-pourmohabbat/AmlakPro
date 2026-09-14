from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [('core', '0003_officeprofile')]
    operations = [
        migrations.AddField(model_name='lead', name='source', field=models.CharField(blank=True, default='website', max_length=40)),
        migrations.AddField(model_name='lead', name='notes', field=models.TextField(blank=True)),
        migrations.AddField(model_name='lead', name='next_follow_up', field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name='lead', name='updated_at', field=models.DateTimeField(auto_now=True)),
        migrations.AddField(model_name='lead', name='assigned_agent', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='core.agent')),
        migrations.CreateModel(name='LeadActivity', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('activity_type', models.CharField(choices=[('call','تماس'),('note','یادداشت'),('visit','بازدید'),('status','تغییر وضعیت')], default='note', max_length=20)),
            ('text', models.TextField()),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='core.lead')),
        ], options={'ordering':['-created_at']})
    ]
