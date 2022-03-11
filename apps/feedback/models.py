from typing import Optional

from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

from apps.feedback.const import DEFAULT_DAYS_OFFSET
from apps.main.models.mixins import BaseModel
from apps.timetables.models import Group


class Profile(BaseModel):
    send_notifications = models.BooleanField(
        verbose_name="Отправлять уведомления?", default=False
    )
    current_group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name="profiles", null=True, blank=True,
        verbose_name="Текущий выбор группы"
    )
    days_offset = models.PositiveSmallIntegerField(
        default=DEFAULT_DAYS_OFFSET,
        verbose_name="Кол-во дней на которое показывать расписание"
    )
    send_notifications_on_lesson_day = models.BooleanField(
        verbose_name="Отправлять уведомления о предстоящих занятиях в день занятий?",
        default=True,
    )
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Аккаунт Django",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.title

    def set_group(self, new: Group) -> None:
        self.current_group = new
        return self.save()

    def get_group(self) -> Optional[Group]:
        return self.current_group

    def get_accounts_in_messengers(self) -> QuerySet:
        return self.messenger_accounts.all()

    def toggle_notifications(self, value: bool) -> None:
        self.send_notifications = value
        return self.save()

    def set_days_offset(self, value: int) -> None:
        self.days_offset = value
        return self.save()


class MessengerModel(BaseModel):
    code = models.CharField(
        verbose_name="Код", max_length=300, default="", unique=True
    )

    class Meta:
        verbose_name = "Мессенджер"
        verbose_name_plural = "Мессенджеры"

    def __str__(self) -> str:
        return self.title


class MessengerAccount(BaseModel):
    messenger = models.ForeignKey(
        MessengerModel, on_delete=models.CASCADE,
        related_name="account", verbose_name="Мессенджер"
    )
    account_id = models.CharField(
        verbose_name="Идентификатор аккаунта в мессенджере",
        max_length=300
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
        related_name="messenger_accounts", verbose_name="Профиль",
        null=True
    )

    class Meta:
        verbose_name = "Аккаунт в мессенджере"
        verbose_name_plural = "Аккаунты в мессенджере"

    def __str__(self) -> str:
        return self.account_id

    def set_profile(self, new: profile) -> None:
        self.profile = new
        return self.save()

    def get_profile(self) -> Optional[Profile]:
        return self.profile

    def get_messenger(self) -> MessengerModel:
        return self.messenger
