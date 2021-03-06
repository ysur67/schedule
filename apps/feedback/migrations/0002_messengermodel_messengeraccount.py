# Generated by Django 4.0 on 2022-01-07 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessengerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Наименование')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Мессенджер',
                'verbose_name_plural': 'Мессенджеры',
            },
        ),
        migrations.CreateModel(
            name='MessengerAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Наименование')),
                ('is_active', models.BooleanField(default=True)),
                ('account_id', models.CharField(max_length=300, verbose_name='Идентификатор аккаунта в мессенджере')),
                ('messenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account', to='feedback.messengermodel', verbose_name='Мессенджер')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messenger_accounts', to='feedback.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Аккаунт в мессенджере',
                'verbose_name_plural': 'Аккаунты в мессенджере',
            },
        ),
    ]
