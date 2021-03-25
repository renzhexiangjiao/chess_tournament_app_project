# Generated by Django 2.2.17 on 2021-03-16 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moveId', models.IntegerField(default=1)),
                ('square_from', models.IntegerField(default=0)),
                ('square_to', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=20)),
                ('player_white', models.CharField(max_length=30)),
                ('player_black', models.CharField(max_length=30)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chess.Tournament')),
            ],
        ),
        migrations.CreateModel(
            name='AccountPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('winRate', models.DecimalField(decimal_places=1, max_digits=3)),
                ('wonGame', models.IntegerField(default=0)),
                ('lostGame', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]