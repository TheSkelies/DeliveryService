from django.db import models
from django.utils import timezone


class PackageQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status="active")

    def completed(self):
        return self.filter(status="completed")

    def cancelled(self):
        return self.filter(status="cancelled")

    def with_related(self):
        return self.select_related("sender", "recipient", "courier")

    def by_courier(self, courier_id: int):
        return self.filter(courier_id=courier_id)

    def arriving_on(self, date_value):
        return self.filter(arrival_date=date_value)

    def available_for_assignment(self):
        """Посылки без курьера и не отменённые — кандидаты на назначение."""
        return self.filter(courier__isnull=True).exclude(status="cancelled")


class PackageManager(models.Manager.from_queryset(PackageQuerySet)):
    pass