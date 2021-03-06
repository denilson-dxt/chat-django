# Generated by Django 3.1.3 on 2020-11-06 18:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0017_auto_20201106_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='friend',
            name='friendship_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 18, 54, 55, 674462, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='message',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 18, 54, 55, 679462, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='receivedrequest',
            name='received_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 18, 54, 55, 679462, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sentrequest',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 18, 54, 55, 679462, tzinfo=utc)),
        ),
    ]
