# Generated by Django 4.2.2 on 2023-10-19 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0004_rental_favorited_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rental',
            name='image10',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='image6',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='image7',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='image8',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='image9',
        ),
    ]