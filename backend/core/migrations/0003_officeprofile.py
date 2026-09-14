from django.db import migrations


class Migration(migrations.Migration):
    """Compatibility migration.

    OfficeProfile is already created by 0001_initial. This migration is
    intentionally a no-op so fresh databases and existing databases follow
    the same migration history without attempting to create the table twice.
    """

    dependencies = [('core', '0002_token')]
    operations = []
