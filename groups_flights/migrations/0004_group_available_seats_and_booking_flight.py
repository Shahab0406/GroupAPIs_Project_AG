from django.db import migrations, models
import django.db.models.deletion


def set_available_seats(apps, schema_editor):
    Group = apps.get_model("groups_flights", "Group")
    for group in Group.objects.all():
        group.available_adult_seats = group.seats
        group.available_child_seats = group.child_seats
        group.save(update_fields=["available_adult_seats", "available_child_seats"])


class Migration(migrations.Migration):

    dependencies = [
        ("groups_flights", "0003_groupbookingdetail"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="available_adult_seats",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Adult seats currently available for booking",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="group",
            name="available_child_seats",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Child seats currently available for booking",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(set_available_seats, migrations.RunPython.noop),
        migrations.AddField(
            model_name="groupbookingdetail",
            name="flight",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="booking_details",
                to="groups_flights.flight",
            ),
        ),
    ]
