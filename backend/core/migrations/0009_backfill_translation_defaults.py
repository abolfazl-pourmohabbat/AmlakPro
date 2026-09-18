from django.db import migrations

def backfill_translations(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("UPDATE core_officeprofile SET translations = '{}'::jsonb WHERE translations IS NULL")
        cursor.execute("UPDATE core_property SET translations = '{}'::jsonb WHERE translations IS NULL")

class Migration(migrations.Migration):
    dependencies = [('core','0008_restore_translation_fields')]
    operations = [migrations.RunPython(backfill_translations, migrations.RunPython.noop)]
