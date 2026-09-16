from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups_flights", "0017_alter_payment_deadlines_to_hours"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="child_seats",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="group",
            name="available_child_seats",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
