from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from couriers.models import Courier
from users.models import User
from .managers import PackageManager

DEFAULT_STATUS = "Ожидает отправки"


class Package(models.Model):
    """Посылка."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Активна"
        CANCELLED = "cancelled", "Отменена"
        COMPLETED = "completed", "Доставлена"

    category = models.CharField(max_length=100, verbose_name="Категория")
    departure_date = models.DateField(verbose_name="Дата отправления")
    arrival_date = models.DateField(verbose_name="Дата прибытия")
    weight = models.FloatField(verbose_name="Вес, кг")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    status = models.CharField(
        max_length=100,
        choices=Status.choices,
        default=Status.ACTIVE,
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
    delivered_flag = models.GeneratedField(
        expression=models.Case(
            models.When(status="completed", then=True),
            default=False,
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Доставлена",
    )

    objects = PackageManager()

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

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"posylka-{self.pk or 'new'}-{slugify(self.category)}"
            self.slug = base
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("packages:detail", kwargs={"slug": self.slug})