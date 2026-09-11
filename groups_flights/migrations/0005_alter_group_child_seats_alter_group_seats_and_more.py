from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("groups_flights", "0004_group_available_seats_and_booking_flight"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="group",
            table="groups",
        ),
        migrations.RenameField(
            model_name="group",
            old_name="seats",
            new_name="adult_seats",
        ),
        migrations.AlterField(
            model_name="group",
            name="adult_seats",
            field=models.PositiveIntegerField(
                help_text="Total number of adult seats in the group",
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="child_seats",
            field=models.PositiveIntegerField(
                help_text="Total number of child seats in the group",
            ),
        ),
        migrations.AlterField(
            model_name="groupbookingdetail",
            name="flight",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="booking_details",
                to="groups_flights.flight",
            ),
        ),
    ]
