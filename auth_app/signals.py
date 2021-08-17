from django.db.models.signals import post_save
from django.dispatch import receiver

from auth_app.models import SellerRequest, Users
from backend.mixins import create_slug
from seller_app.models import Shop


@receiver(post_save, sender=SellerRequest)
def seller_req(sender, instance, created, **kwargs):
    if not created:
        if instance.accepted and Users.objects.filter(phone_number=instance.contact_number).count() == 0:
            seller = Users.objects.create_seller(name=instance.seller_name, phone_number=instance.contact_number,
                                                 password='12345678')
            shop = Shop.objects.create(
                name=instance.shop_name,
                contact_number=instance.contact_number,
                business_location=instance.shop_business_address,
                active=True,
                seller=seller,
                category=instance.category_option,
            )
