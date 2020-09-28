# Generated by Django 3.0.4 on 2020-03-16 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_customer_stock_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfoliodata',
            name='tutorial_slug',
        ),
        migrations.AddField(
            model_name='portfoliodata',
            name='current_quantity',
            field=models.IntegerField(default=100),
        ),
    ]
