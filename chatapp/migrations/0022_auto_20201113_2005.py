# Generated by Django 3.1.3 on 2020-11-14 04:05

import cloudinary.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0021_auto_20201107_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='perfil_picture',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='friendship_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 14, 4, 5, 1, 353389, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='message',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 14, 4, 5, 1, 353389, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='publication',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 14, 4, 5, 1, 353389, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='receivedrequest',
            name='received_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 14, 4, 5, 1, 353389, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sentrequest',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 14, 4, 5, 1, 353389, tzinfo=utc)),
        ),
    ]
