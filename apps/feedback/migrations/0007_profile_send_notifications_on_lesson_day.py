# Generated by Django 4.0 on 2022-01-21 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0006_profile_days_offset'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='send_notifications_on_lesson_day',
            field=models.BooleanField(default=True, verbose_name='Отправлять уведомления о предстоящих занятиях в день занятий?'),
        ),
    ]
