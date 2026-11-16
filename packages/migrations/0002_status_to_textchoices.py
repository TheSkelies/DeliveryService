from django.db import migrations


STATUS_MAP = {
    "Ожидает отправки": "active",
    "Package at the drop-off point": "active",
    "В пути": "active",
    "In transit": "active",
    "Доставлена": "completed",
    "Delivered": "completed",
    "Отменена": "cancelled",
    "Cancelled": "cancelled",
}


def forwards(apps, schema_editor):
    Package = apps.get_model("packages", "Package")
    for p in Package.objects.all():
        new = STATUS_MAP.get(p.status, "active")
        if p.status != new:
            p.status = new
            p.save(update_fields=["status"])


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("packages", "0001_initial")]
    operations = [migrations.RunPython(forwards, backwards)]