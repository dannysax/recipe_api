# Generated by Django 3.2.15 on 2022-09-23 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_user_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
    ]