from django.db.models.signals import pre_save
from django.dispatch import receiver

from admin_app.models import ShopCategory, Category
from backend.mixins import create_slug


@receiver(pre_save, sender=ShopCategory)
def shop_cat_slug(sender, instance, *args, **kwargs):
    print(instance)
    instance.slug = create_slug(instance, instance.name)


@receiver(pre_save, sender=Category)
def cat_slug(sender, instance, *args, **kwargs):
    instance.slug = create_slug(instance, instance.name)
