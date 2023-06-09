# Generated by Django 4.1 on 2023-03-14 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tail_number', models.CharField(max_length=20)),
                ('serial_number', models.CharField(max_length=50)),
                ('aircraft_type', models.CharField(max_length=100)),
                ('year_of_production', models.CharField(max_length=10)),
                ('photo1', models.URLField(blank=True, null=True)),
                ('photo2', models.URLField(blank=True, null=True)),
                ('photo3', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
