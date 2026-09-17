from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groups_flights", "0015_remove_group_is_published"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="groupbookingdetail",
            name="flight",
        ),
    ]
