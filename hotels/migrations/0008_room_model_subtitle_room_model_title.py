# Generated by Django 5.1.3 on 2025-01-25 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0007_roomimage_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='room_model',
            name='subtitle',
            field=models.TextField(blank=True, help_text='Room subtitle', null=True),
        ),
        migrations.AddField(
            model_name='room_model',
            name='title',
            field=models.CharField(blank=True, help_text='Room title', max_length=255, null=True),
        ),
    ]
