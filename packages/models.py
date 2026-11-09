from django.db import models

from couriers.models import Courier
from users.models import User

DEFAULT_STATUS = "Ожидает отправки"


class Package(models.Model):
    """Посылка."""

    category = models.CharField(max_length=100, verbose_name="Категория")
    departure_date = models.DateField(verbose_name="Дата отправления")
    arrival_date = models.DateField(verbose_name="Дата прибытия")
    weight = models.FloatField(verbose_name="Вес, кг")
    status = models.CharField(
        max_length=100,
        default=DEFAULT_STATUS,
        verbose_name="Статус",
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="sent_packages",
        null=True,
        blank=True,
        verbose_name="Отправитель",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="received_packages",
        null=True,
        blank=True,
        verbose_name="Получатель",
    )
    courier = models.ForeignKey(
        Courier,
        on_delete=models.SET_NULL,
        related_name="packages",
        null=True,
        blank=True,
        verbose_name="Доставщик",
    )

    def __str__(self) -> str:
        sender = self.sender.name if self.sender else "—"
        recipient = self.recipient.name if self.recipient else "—"
        return f"#{self.pk} [{self.category}] {sender} -> {recipient}"

    def is_delivered(self) -> bool:
        return "доставлена" in self.status.lower()

    class Meta:
        ordering = ["id"]
        verbose_name = "Посылка"
        verbose_name_plural = "Посылки"