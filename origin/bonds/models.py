from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import get_legal_name


class Bond(models.Model):
    isin = models.CharField(max_length=50)
    size = models.BigIntegerField()
    currency = models.CharField(max_length=3)
    maturity = models.DateField()
    lei = models.CharField(max_length=50)
    legal_name = models.CharField(max_length=200)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Bond {self.isin}"


@receiver(pre_save, sender=Bond)
def set_legal_name(sender, instance, **kwargs):
    """
    if legal name missing, call an API to retrieve
    """
    if not instance.legal_name:
        legal_name = get_legal_name(instance.lei)
        instance.legal_name = legal_name
