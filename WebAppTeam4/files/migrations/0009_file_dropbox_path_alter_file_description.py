# Generated by Django 4.2.4 on 2023-09-10 22:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('files', '0008_file_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='dropbox_path',
            field=models.CharField(default=''),
        ),
        migrations.AlterField(
            model_name='file',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
