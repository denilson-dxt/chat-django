# Generated by Django 3.1.3 on 2020-11-05 11:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0007_friend_recivedrequest_sentrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='friendship_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 5, 11, 38, 17, 48070, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sentrequest',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 5, 11, 38, 17, 48070, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='RecivedRequest',
        ),
    ]
