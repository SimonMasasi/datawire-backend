# Generated by Django 5.0.4 on 2024-05-09 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetApp', '0006_modelfile_model_architecture_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='model',
            old_name='name',
            new_name='title',
        ),
    ]
