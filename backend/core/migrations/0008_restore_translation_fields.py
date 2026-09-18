from django.db import migrations, models

def ensure_translation_columns(apps, schema_editor):
    connection = schema_editor.connection
    cursor = connection.cursor()
    existing = {column.name for column in connection.introspection.get_table_description(cursor, 'core_officeprofile')}
    if 'translations' not in existing:
        field = models.JSONField(default=dict, blank=True)
        field.set_attributes_from_name('translations')
        schema_editor.add_field(apps.get_model('core', 'OfficeProfile'), field)

    existing = {column.name for column in connection.introspection.get_table_description(cursor, 'core_property')}
    if 'translations' not in existing:
        field = models.JSONField(default=dict, blank=True)
        field.set_attributes_from_name('translations')
        schema_editor.add_field(apps.get_model('core', 'Property'), field)

    with connection.cursor() as cursor:
        cursor.execute("UPDATE core_officeprofile SET translations = '{}'::jsonb WHERE translations IS NULL")
        cursor.execute("UPDATE core_property SET translations = '{}'::jsonb WHERE translations IS NULL")

class Migration(migrations.Migration):
    dependencies = [('core','0007_contact_labels')]
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[migrations.RunPython(ensure_translation_columns, migrations.RunPython.noop)],
            state_operations=[
                migrations.AddField(model_name='officeprofile', name='translations', field=models.JSONField(blank=True, default=dict)),
                migrations.AddField(model_name='property', name='translations', field=models.JSONField(blank=True, default=dict)),
            ],
        ),
    ]
