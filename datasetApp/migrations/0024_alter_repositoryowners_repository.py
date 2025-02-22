# Generated by Django 5.0.6 on 2024-07-04 07:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasetApp', '0023_alter_repositoryowners_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repositoryowners',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_repository', to='datasetApp.repository'),
        ),
    ]
