# Generated by Django 4.2.7 on 2025-02-25 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_bot_game',
            field=models.BooleanField(default=False),
        ),
    ]
