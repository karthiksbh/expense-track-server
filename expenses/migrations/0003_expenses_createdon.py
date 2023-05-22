# Generated by Django 4.2.1 on 2023-05-22 16:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0002_expenses_user_ref"),
    ]

    operations = [
        migrations.AddField(
            model_name="expenses",
            name="createdOn",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
