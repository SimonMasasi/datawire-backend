# Generated by Django 5.0.6 on 2024-07-04 06:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasetApp', '0021_modelschatroom_modelchatmessages'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repository',
            name='owner',
        ),
        migrations.CreateModel(
            name='RepositoryOwners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasetApp.repository')),
            ],
        ),
    ]
