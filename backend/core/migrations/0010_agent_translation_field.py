from django.db import migrations, models

def ensure_agent_translation_column(apps, schema_editor):
    connection = schema_editor.connection
    cursor = connection.cursor()
    columns = {c.name for c in connection.introspection.get_table_description(cursor, 'core_agent')}
    if 'translations' not in columns:
        field = models.JSONField(default=dict, blank=True)
        field.set_attributes_from_name('translations')
        schema_editor.add_field(apps.get_model('core', 'Agent'), field)
    apps.get_model('core', 'Agent').objects.filter(translations__isnull=True).update(translations={})

class Migration(migrations.Migration):
    dependencies = [('core','0009_backfill_translation_defaults')]
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[migrations.RunPython(ensure_agent_translation_column, migrations.RunPython.noop)],
            state_operations=[migrations.AddField(model_name='agent',name='translations',field=models.JSONField(blank=True,default=dict))],
        ),
    ]
