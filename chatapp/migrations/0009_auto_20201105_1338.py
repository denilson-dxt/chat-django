# Generated by Django 3.1.3 on 2020-11-05 11:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0008_auto_20201105_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='friendship_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 5, 11, 38, 29, 614189, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sentrequest',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 5, 11, 38, 29, 614189, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='ReceivedRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_day', models.DateTimeField(default=datetime.datetime(2020, 11, 5, 11, 38, 29, 614189, tzinfo=utc))),
                ('long_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('acepted', models.BooleanField(default=False)),
                ('denied', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatapp.usersystem')),
            ],
        ),
    ]
