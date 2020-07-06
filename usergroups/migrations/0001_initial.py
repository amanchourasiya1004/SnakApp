# Generated by Django 3.0.2 on 2020-07-05 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupname', models.CharField(max_length=20, unique=True)),
                ('timeCreation', models.DateTimeField(auto_now_add=True)),
                ('participants', models.IntegerField(default=0)),
                ('description', models.CharField(default='-', max_length=50)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='GroupUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeCreation', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupusers', to='usergroups.Groups')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupenrolled', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UserGroups',
            },
        ),
        migrations.CreateModel(
            name='GroupChats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chats', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='usergroups.Groups')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'GroupChats',
            },
        ),
    ]
