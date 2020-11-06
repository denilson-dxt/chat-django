# Generated by Django 3.1.3 on 2020-11-06 21:48

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0018_auto_20201106_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='friendship_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 21, 48, 1, 377247, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='message',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 21, 48, 1, 377247, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='receivedrequest',
            name='received_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 21, 48, 1, 377247, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sentrequest',
            name='sent_day',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 21, 48, 1, 377247, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField()),
                ('likes', models.PositiveIntegerField(default=0)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2020, 11, 6, 21, 48, 1, 377247, tzinfo=utc))),
                ('user_system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatapp.usersystem')),
            ],
        ),
    ]
