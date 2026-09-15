import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups_flights", "0010_remove_groupbookingdetail_flight"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="group",
            name="token_payment_deadline",
        ),
        migrations.RemoveField(
            model_name="group",
            name="full_payment_deadline",
        ),
        migrations.AddField(
            model_name="group",
            name="token_payment_deadline",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
        migrations.AddField(
            model_name="group",
            name="full_payment_deadline",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
        migrations.RemoveField(
            model_name="groupbookingdetail",
            name="token_payment_deadline",
        ),
        migrations.RemoveField(
            model_name="groupbookingdetail",
            name="full_payment_deadline",
        ),
        migrations.AddField(
            model_name="groupbookingdetail",
            name="token_payment_deadline",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
        migrations.AddField(
            model_name="groupbookingdetail",
            name="full_payment_deadline",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
    ]
