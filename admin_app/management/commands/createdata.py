from django.core.management.base import BaseCommand

from auth_app.models import Users
from faker import Faker
from admin_app.models import Category, ShopCategory, ProductVariationAdmin

fake = Faker()


class Command(BaseCommand):
    help = "command information"
    users_id = Users.objects.filter(seller=False).values_list('id', flat=True)
    seller_id = Users.objects.filter(seller=True).values_list('id', flat=True)

    def handle(self, *args, **options):
        inserted_pks = populator.execute()
