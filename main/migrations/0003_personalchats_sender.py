# Generated by Django 3.0.2 on 2020-07-10 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200705_0617'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalchats',
            name='sender',
            field=models.CharField(default='-', max_length=20),
        ),
    ]