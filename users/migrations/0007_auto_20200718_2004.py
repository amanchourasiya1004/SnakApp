# Generated by Django 3.0.2 on 2020-07-18 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_profilepic'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProfilePic',
        ),
        migrations.AddField(
            model_name='users',
            name='profilepic',
            field=models.TextField(default='-'),
        ),
    ]
