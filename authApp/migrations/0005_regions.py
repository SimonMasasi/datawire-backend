# Generated by Django 5.0.6 on 2024-07-03 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0004_remove_chatroom_creator_remove_chatroom_receiver_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=9000, unique=True)),
            ],
        ),
    ]
