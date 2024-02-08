# Generated by Django 5.0.1 on 2024-02-06 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True)),
                ('is_mvp', models.BooleanField(blank=True, default=False)),
                ('hire_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]