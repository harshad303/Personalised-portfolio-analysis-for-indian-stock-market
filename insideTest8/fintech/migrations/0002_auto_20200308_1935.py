# Generated by Django 3.0.4 on 2020-03-08 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fintech', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='name',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='destination',
            name='price',
            field=models.IntegerField(default=100),
        ),
    ]
