from abc import abstractmethod
from django.db import models


class TitleMixin(models.Model):
    title = models.CharField(
        verbose_name="Наименование", max_length=300
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title


class IsActiveMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class LoggingMixin(models.Model):

    class Meta:
        abstract = True

    @abstractmethod
    def to_logging_message(self) -> str:
        pass


class BaseModel(TitleMixin, IsActiveMixin, LoggingMixin):

    class Meta:
        abstract = True

    def to_logging_message(self) -> str:
        msg = f"Объект: {self.Meta.verbose_name}\n" + \
        f"Наименование: {self.title}\n"
        return msg
