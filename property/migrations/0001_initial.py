# Generated by Django 4.1.7 on 2023-04-03 11:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('num_of_rooms', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('location', models.CharField(max_length=255)),
                ('lease_term_in_months', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('is_lease_term_negotiable', models.BooleanField(default=False)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=15)),
                ('is_rate_negotiable', models.BooleanField(default=False)),
                ('is_furnished', models.BooleanField(verbose_name=False)),
                ('image1', models.URLField()),
                ('image2', models.URLField()),
                ('image3', models.URLField()),
                ('image4', models.URLField()),
                ('image5', models.URLField()),
                ('image6', models.URLField(blank=True, null=True)),
                ('image7', models.URLField(blank=True, null=True)),
                ('image8', models.URLField(blank=True, null=True)),
                ('image9', models.URLField(blank=True, null=True)),
                ('image10', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]