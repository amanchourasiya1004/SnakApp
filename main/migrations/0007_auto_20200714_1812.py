# Generated by Django 3.0.2 on 2020-07-14 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_imageupload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageupload',
            name='chatconnect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sentimages', to='main.Friends'),
        ),
    ]
