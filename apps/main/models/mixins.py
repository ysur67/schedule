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


class BaseModel(TitleMixin, IsActiveMixin):

    class Meta:
        abstract = True
