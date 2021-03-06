# Generated by Django 3.1.3 on 2020-11-06 08:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0016_auto_20201105_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatapp.usersystem')),
            ],
        ),
        migrations.AlterField(
            model_name='friend',
            name='friendship_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 8, 47, 53, 334192, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='receivedrequest',
            name='received_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 8, 47, 53, 334192, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sentrequest',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 8, 47, 53, 334192, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('sent_day', models.DateTimeField(default=datetime.datetime(2020, 11, 6, 8, 47, 53, 334192, tzinfo=utc))),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatapp.chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
