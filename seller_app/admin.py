from django.contrib import admin

# Register your models here.
from backend.mixins import ExportCsvMixin
from seller_app.models import Shop, Product, ProductOption, ProductVariance, ProductImage


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin, ExportCsvMixin):

    list_display = (
        'name',
        'slug',
        'seller',
        'contact_number',
        'banner',
        'category',
        'business_location',
        'active',
        'date_joined',
        'updated',
    )
    actions = ["export_as_csv"]


@admin.register(Product)
class ShopAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'name',
        'slug',
        'seller',
        'shop',
        'product_price',
        'selling_price',
        'quantity',
        'active',
        'description',
        'offer_price',
        'offer_price_start',
        'offer_price_end',
        'date_joined',
        'updated',
        'trash',
    )
    actions = ["export_as_csv"]


@admin.register(ProductOption)
class ShopAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'product',
        'option',
    )
    actions = ["export_as_csv"]


@admin.register(ProductVariance)
class ShopAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'product',
        'variance',
        'color',
        'size',
        'product_price',
        'selling_price',
        'quantity',
    )
    actions = ["export_as_csv"]


@admin.register(ProductImage)
class ShopAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'product',
        'image',
    )
    actions = ["export_as_csv"]
