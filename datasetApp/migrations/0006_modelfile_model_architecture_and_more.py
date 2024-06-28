# Generated by Django 5.0.4 on 2024-05-09 18:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasetApp', '0005_dataset_total_files'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(null=True, upload_to='models/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='model',
            name='architecture',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='model',
            name='performance_metrics',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ModelFileExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extension', models.CharField(max_length=10)),
                ('file', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='datasetApp.file')),
            ],
        ),
        migrations.CreateModel(
            name='ModelVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upvoted_at', models.DateTimeField(auto_now_add=True)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='datasetApp.model')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('model', 'user')},
            },
        ),
    ]
