# Generated by Django 5.1.3 on 2025-01-24 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_remove_hotel_model_available_rooms_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_model',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='rooms/image/'),
        ),
    ]
