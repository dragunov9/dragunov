# Generated by Django 5.2.1 on 2025-06-27 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
