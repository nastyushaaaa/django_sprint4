# Generated by Django 3.2.16 on 2023-07-14 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_crecreated_at_location_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='autor',
            new_name='author',
        ),
    ]