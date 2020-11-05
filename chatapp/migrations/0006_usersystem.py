# Generated by Django 3.1.3 on 2020-11-05 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_delete_usersystem'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
