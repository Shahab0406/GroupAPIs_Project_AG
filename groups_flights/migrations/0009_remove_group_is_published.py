from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groups_flights", "0008_alter_groupbookingdetail_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="group",
            name="is_published",
        ),
    ]
