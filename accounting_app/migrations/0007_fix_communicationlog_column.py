# Fix the recipient_client_id column rename to recipient_beneficiary_id

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_app', '0006_rename_communicationlog_recipient_client'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE accounting_app_communicationlog RENAME COLUMN recipient_client_id TO recipient_beneficiary_id;",
            reverse_sql="ALTER TABLE accounting_app_communicationlog RENAME COLUMN recipient_beneficiary_id TO recipient_client_id;"
        ),
    ]
