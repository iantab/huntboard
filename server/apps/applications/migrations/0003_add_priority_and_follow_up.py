from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0002_add_status_history"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="priority",
            field=models.CharField(
                choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
                default="medium",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="application",
            name="follow_up_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
