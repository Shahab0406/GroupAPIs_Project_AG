from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groups_flights", "0005_alter_group_child_seats_alter_group_seats_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="groupbookingdetail",
            old_name="requested_adult_seats",
            new_name="adult_seats_requested",
        ),
        migrations.RenameField(
            model_name="groupbookingdetail",
            old_name="requested_child_seats",
            new_name="child_seats_requested",
        ),
    ]
