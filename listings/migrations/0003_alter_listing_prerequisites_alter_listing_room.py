# Generated by Django 5.0.1 on 2024-02-06 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_alter_listing_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='prerequisites',
            field=models.CharField(blank=True, max_length=35),
        ),
        migrations.AlterField(
            model_name='listing',
            name='room',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
