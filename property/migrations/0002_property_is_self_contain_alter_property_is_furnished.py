# Generated by Django 4.1.7 on 2023-04-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='is_self_contain',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='property',
            name='is_furnished',
            field=models.BooleanField(default=False),
        ),
    ]