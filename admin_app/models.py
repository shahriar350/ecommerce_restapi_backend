from django.db import models


# Create your models here.
class ShopCategory(models.Model):
    name = models.CharField(max_length=110, verbose_name='Shop Category name')
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category name')
    slug = models.SlugField(unique=True, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='subcategory')
    shop = models.ForeignKey(ShopCategory, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="get_category")

    def __str__(self):
        return self.name


class ProductVariationAdmin(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=150)
    shop = models.ForeignKey(ShopCategory, on_delete=models.CASCADE, related_name='get_category_shop')

    def __str__(self):
        return self.name
