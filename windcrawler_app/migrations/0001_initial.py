# Generated by Django 3.1 on 2020-09-08 18:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('api_key', models.TextField(blank=True)),
                ('url', models.CharField(blank=True, max_length=300)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wooi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('handle', models.CharField(max_length=100)),
                ('legal', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('nav_link', models.CharField(blank=True, max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('historical_available', models.BooleanField(default=False)),
                ('source_api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='windcrawler_app.sources')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.CharField(max_length=100)),
                ('gust', models.FloatField(default=0)),
                ('wind', models.FloatField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='windcrawler_app.wooi')),
            ],
        ),
    ]