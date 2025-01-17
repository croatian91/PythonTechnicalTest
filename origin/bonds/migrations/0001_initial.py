# Generated by Django 2.2.13 on 2020-12-31 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bond",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("isin", models.CharField(max_length=50)),
                ("size", models.BigIntegerField()),
                ("currency", models.CharField(max_length=3)),
                ("maturity", models.DateField()),
                ("lei", models.CharField(max_length=50)),
                ("legal_name", models.CharField(max_length=200)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
