import json

from django.db.models.signals import pre_save
from django.dispatch import receiver

from backend.mixins import create_slug
from seller_app.models import Shop, Product


@receiver(pre_save, sender=Shop)
def shop_slug_create(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance, instance.name)

@receiver(pre_save, sender=Product)
def shop_slug_create(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = create_slug(instance, instance.name)

