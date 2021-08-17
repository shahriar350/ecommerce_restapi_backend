from django.contrib import admin

# Register your models here.
from auth_app.models import SellerRequest, Users
from backend.mixins import ExportCsvMixin


@admin.register(SellerRequest)
class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'seller_name',
        'shop_name',
        'contact_location',
        'contact_number',
        'shop_business_address',
        'category_option',
        'accepted',
        'accept_by',
    )
    actions = ["export_as_csv"]


@admin.register(Users)
class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'name',
        'phone_number',
        'admin',
        'seller',
        'active',
        'staff',
        'is_verified',
        'date_joined',
    )
    actions = ["export_as_csv"]
