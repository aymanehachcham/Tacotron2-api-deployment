# Generated by Django 3.1.4 on 2020-12-16 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ttssound',
            name='name',
        ),
    ]
