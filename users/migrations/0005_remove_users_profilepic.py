# Generated by Django 3.0.2 on 2020-07-18 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_users_profilepic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='profilepic',
        ),
    ]
