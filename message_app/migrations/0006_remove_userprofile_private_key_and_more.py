# Generated by Django 4.1.5 on 2023-05-17 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("message_app", "0005_userprofile_private_key_userprofile_public_key"),
    ]

    operations = [
        migrations.RemoveField(model_name="userprofile", name="private_key",),
        migrations.RemoveField(model_name="userprofile", name="public_key",),
        migrations.AddField(
            model_name="userprofile",
            name="group_key",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
