# Generated by Django 5.0.4 on 2024-05-10 19:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasetApp', '0012_alter_modelfileextension_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelfile',
            name='model',
        ),
        migrations.CreateModel(
            name='ModelFolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datasetApp.model')),
                ('parent_folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datasetApp.modelfolder')),
            ],
        ),
        migrations.AddField(
            model_name='modelfile',
            name='folder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='datasetApp.modelfolder'),
        ),
    ]
