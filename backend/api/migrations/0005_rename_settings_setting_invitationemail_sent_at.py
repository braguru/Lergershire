# Generated by Django 4.2.6 on 2023-10-28 23:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_settings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Settings',
            new_name='Setting',
        ),
        migrations.AddField(
            model_name='invitationemail',
            name='sent_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
