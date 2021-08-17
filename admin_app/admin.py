from django.contrib import admin

# Register your models here.

# Register your models here.
from admin_app.models import ShopCategory, Category, ProductVariationAdmin, Brand
from backend.mixins import ExportCsvMixin


@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'name',
        'slug',
        'image'
    )
    actions = ["export_as_csv"]


class ShopAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ShopAdmin(admin.ModelAdmin):
    search_fields = ['shop__name']


class ParentAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Category)
class ShopCategoryAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['name']
    autocomplete_fields = ['parent']
    list_display = (
        'name',
        'slug',
        'parent',
        'shop',
    )
    actions = ["export_as_csv"]


@admin.register(ProductVariationAdmin)
class ProductVariationAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name',)
    actions = ['export_as_csv']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'shop',)
    actions = ['export_as_csv']
