# Generated by Django 4.1.5 on 2023-01-13 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='title',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='content',
        ),
    ]
