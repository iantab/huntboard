from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0003_add_priority_and_follow_up"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="salary_min",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="application",
            name="salary_max",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
