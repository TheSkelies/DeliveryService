from django.db import models


class User(models.Model):
    """Пользователь предметной области: отправитель или получатель."""

    name = models.CharField(
        max_length=200,
        verbose_name="Имя пользователя",
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"