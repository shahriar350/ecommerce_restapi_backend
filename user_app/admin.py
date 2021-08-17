from django.contrib import admin

# Register your models here.
from backend.mixins import ExportCsvMixin
from user_app.models import Cart, CartProduct, UserLocation, Checkout, CheckoutProduct


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'slug',
        'user',
        'date_joined',
        'updated',
        'active',
    )
    actions = ["export_as_csv"]


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'cart',
        'product',
        'variation',
        'quantity',

    )
    actions = ["export_as_csv"]


@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'user',
        'area',
        'street',
        'house',
        'post_office',
        'post_code',
        'police_station',
        'city',
    )
    actions = ["export_as_csv"]


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'slug',
        'user',
        'cart',
        'created',
        'updated',
        'total_price',
        'location',
        'completed',
    )
    actions = ["export_as_csv"]


@admin.register(CheckoutProduct)
class CheckoutProductAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'slug',
        'checkout',
        'product',
        'selling_price',
        'offer_price',
        'quantity',
        'created',
        'updated',
        'received',
        'status',
    )
    actions = ["export_as_csv"]
