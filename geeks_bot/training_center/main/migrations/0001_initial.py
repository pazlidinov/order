# Generated by Django 4.2.16 on 2024-10-09 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('duration', models.CharField(max_length=150)),
                ('times_in_week', models.IntegerField(default=0)),
                ('time_of_lesson', models.TimeField()),
                ('price', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=0)),
                ('info', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('telegram_id', models.BigIntegerField(default=1, unique=True)),
                ('phone', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='main.course')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customers', to='main.customer')),
            ],
        ),
    ]
