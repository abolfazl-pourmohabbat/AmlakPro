from django.db import migrations

def backfill_translations(apps, schema_editor):
    apps.get_model('core', 'OfficeProfile').objects.filter(translations__isnull=True).update(translations={})
    apps.get_model('core', 'Property').objects.filter(translations__isnull=True).update(translations={})

class Migration(migrations.Migration):
    dependencies = [('core','0008_restore_translation_fields')]
    operations = [migrations.RunPython(backfill_translations, migrations.RunPython.noop)]
