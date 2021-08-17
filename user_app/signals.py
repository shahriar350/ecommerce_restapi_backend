import uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver

from backend.mixins import create_slug
from user_app.models import Cart


@receiver(pre_save, sender=Cart)
def shop_slug_create(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = create_slug(instance, uuid.uuid4())
