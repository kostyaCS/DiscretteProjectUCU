# Generated by Django 4.1.5 on 2023-05-12 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("message_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="message_images/"),
        ),
    ]
