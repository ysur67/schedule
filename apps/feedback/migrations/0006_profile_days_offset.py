# Generated by Django 4.0 on 2022-01-19 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_profile_current_group_profile_send_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='days_offset',
            field=models.PositiveSmallIntegerField(default=7, verbose_name='Кол-во дней на которое показывать расписание'),
        ),
    ]