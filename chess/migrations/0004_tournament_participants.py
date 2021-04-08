# Generated by Django 2.2.17 on 2021-04-07 15:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chess', '0003_auto_20210407_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='participants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
