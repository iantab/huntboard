from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0004_add_salary_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="status",
            field=models.CharField(
                choices=[
                    ("wishlist", "Wishlist"),
                    ("applied", "Applied"),
                    ("phone_screen", "Phone Screen"),
                    ("interview", "Interview"),
                    ("offer", "Offer"),
                    ("rejected", "Rejected"),
                    ("closed", "Closed"),
                ],
                db_index=True,
                default="wishlist",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="application",
            name="follow_up_date",
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
    ]
