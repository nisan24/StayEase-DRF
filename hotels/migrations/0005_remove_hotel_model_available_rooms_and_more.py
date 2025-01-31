# Generated by Django 5.1.3 on 2025-01-23 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_hotelimage_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel_model',
            name='available_rooms',
        ),
        migrations.RemoveField(
            model_name='hotel_model',
            name='price_per_night',
        ),
        migrations.AddField(
            model_name='hotel_model',
            name='price_range_max',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='hotel_model',
            name='price_range_min',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.CreateModel(
            name='Room_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amenities', models.TextField()),
                ('guests', models.PositiveIntegerField(help_text='Maximum number of guests')),
                ('bedrooms', models.PositiveIntegerField(help_text='Number of bedrooms')),
                ('beds', models.PositiveIntegerField(help_text='Number of beds')),
                ('bathrooms', models.PositiveIntegerField(default=1, help_text='Number of bathrooms')),
                ('available_rooms', models.PositiveIntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='hotels/rooms/image/')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotels.hotel_model')),
            ],
        ),
    ]
