# Generated by Django 4.0.3 on 2025-01-01 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='telegram_id',
        ),
    ]