# Generated by Django 4.1.7 on 2023-04-03 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='review_owner',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='agent',
            new_name='user_reviewed',
        ),
    ]