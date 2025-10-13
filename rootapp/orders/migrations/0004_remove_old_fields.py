from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orderstatus_order_status'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE orders_order DROP COLUMN is_new;",
            reverse_sql="ALTER TABLE orders_order ADD COLUMN is_new BOOLEAN DEFAULT TRUE;"
        ),
        migrations.RunSQL(
            "ALTER TABLE orders_order DROP COLUMN checked_by_task;", 
            reverse_sql="ALTER TABLE orders_order ADD COLUMN checked_by_task BOOLEAN DEFAULT FALSE;"
        ),
        migrations.RunSQL(
            "ALTER TABLE orders_order DROP COLUMN payment_status;",
            reverse_sql="ALTER TABLE orders_order ADD COLUMN payment_status VARCHAR(20) DEFAULT 'pending';"
        ),
        migrations.RunSQL(
            "ALTER TABLE orders_order DROP COLUMN processing_status;",
            reverse_sql="ALTER TABLE orders_order ADD COLUMN processing_status VARCHAR(20) DEFAULT 'new';"
        ),
        migrations.RunSQL(
            "ALTER TABLE orders_order DROP COLUMN was_seen;",
            reverse_sql="ALTER TABLE orders_order ADD COLUMN was_seen BOOLEAN DEFAULT FALSE;"
        ),
    ]