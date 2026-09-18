from django.db import migrations, models

def ensure_agent_translation_column(apps, schema_editor):
    connection = schema_editor.connection
    cursor = connection.cursor()
    columns = {c.name for c in connection.introspection.get_table_description(cursor, 'core_agent')}
    Agent = apps.get_model('core', 'Agent')
    if 'translations' not in columns:
        schema_editor.add_field(Agent, Agent._meta.get_field('translations'))
    cursor.execute("UPDATE core_agent SET translations = '{}'::jsonb WHERE translations IS NULL")

class Migration(migrations.Migration):
    dependencies = [('core','0009_backfill_translation_defaults')]
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[migrations.RunPython(ensure_agent_translation_column, migrations.RunPython.noop)],
            state_operations=[migrations.AddField(model_name='agent',name='translations',field=models.JSONField(blank=True,default=dict))],
        ),
    ]
