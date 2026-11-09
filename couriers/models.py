from django.db import models
from django.utils.functional import cached_property


class Courier(models.Model):
    """Доставщик."""

    name = models.CharField(max_length=200, verbose_name="Имя доставщика")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    vehicle = models.CharField(max_length=30, verbose_name="Транспорт")
    departure_date = models.DateField(verbose_name="Дата выезда")
    expected_delivery_date = models.DateField(
        verbose_name="Примерная дата доставки",
    )
    capacity_kg = models.FloatField(
        default=50.0,
        verbose_name="Грузоподъёмность, кг",
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступен",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.vehicle})"

    @cached_property
    def total_weight(self) -> float:
        total = self.packages.aggregate(
            total=models.Sum("weight")
        )["total"]
        return total or 0.0

    def can_take_package(self, package) -> bool:
        if not self.is_available:
            return False
        if package.arrival_date != self.expected_delivery_date:
            return False
        return self.total_weight + package.weight <= self.capacity_kg

    def can_take_package(self, package) -> bool:
        """Может ли доставщик взять посылку (бизнес-правило ПР3)."""
        if not self.is_available:
            return False
        if package.arrival_date != self.expected_delivery_date:
            return False
        return self.total_weight + package.weight <= self.capacity_kg

    class Meta:
        ordering = ["name"]
        verbose_name = "Доставщик"
        verbose_name_plural = "Доставщики"