# Generated by Django 3.1.3 on 2020-11-16 17:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0023_auto_20201114_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='last_message',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='friend',
            name='friendship_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 16, 17, 45, 50, 213120, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='message',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 16, 17, 45, 50, 213120, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='publication',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 16, 17, 45, 50, 213120, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='receivedrequest',
            name='received_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 16, 17, 45, 50, 213120, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sentrequest',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 16, 17, 45, 50, 213120, tzinfo=utc)),
        ),
    ]
