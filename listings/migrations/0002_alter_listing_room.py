# Generated by Django 5.0.1 on 2024-02-06 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='room',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]