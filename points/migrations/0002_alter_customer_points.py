# Generated by Django 4.0.2 on 2022-02-08 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
