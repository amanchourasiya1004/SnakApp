# Generated by Django 3.0.2 on 2020-07-05 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usergroups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='groups',
            name='participants',
            field=models.TextField(default='-'),
        ),
    ]
