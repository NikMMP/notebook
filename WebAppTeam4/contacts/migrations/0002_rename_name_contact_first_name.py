# Generated by Django 4.2.4 on 2023-09-03 03:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='name',
            new_name='first_name',
        ),
    ]
