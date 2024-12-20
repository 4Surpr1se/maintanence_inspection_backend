# Generated by Django 5.1.4 on 2024-12-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aircraft",
            name="aircraft_sn",
            field=models.CharField(
                default=None, max_length=255, unique=True, verbose_name="Aircraft SN"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="work",
            name="mh",
            field=models.IntegerField(default=7, verbose_name="MH"),
        ),
    ]
