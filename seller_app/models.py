from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db.models import Max, Min

from admin_app.models import ShopCategory, Category, ProductVariationAdmin, Brand
from auth_app.models import Users
from datetime import date


class Shop(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    seller = models.ForeignKey(Users, null=True,
                               limit_choices_to={'seller': True},
                               on_delete=models.SET_NULL,
                               related_name="get_seller")
    contact_number = models.CharField(max_length=11)
    banner = models.ImageField()
    category = models.ForeignKey(ShopCategory, on_delete=models.SET_NULL, null=True,
                                 related_name="get_shop")
    business_location = models.TextField()
    active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    trash = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    seller = models.ForeignKey(Users, null=True,
                               limit_choices_to={'seller': True},
                               on_delete=models.SET_NULL,
                               related_name="get_product_seller")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, related_name="get_product_shop")
    product_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0)])
    active = models.BooleanField(default=True)
    description = models.TextField()
    offer_price = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    offer_price_start = models.DateField(null=True, blank=True)
    offer_price_end = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    next_stock_date = models.DateField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    trash = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, related_name='get_brand', on_delete=models.CASCADE, null=True,blank=True)

    @property
    def is_offer_valid(self):
        if self.offer_price_start is not None and self.offer_price_end is not None:
            return self.offer_price_start <= date.today() <= self.offer_price_end
        else:
            return False

    @property
    def first_price(self):
        if not self.get_product_variation.exists():
            if self.is_offer_valid:
                return self.selling_price - (self.selling_price * (self.offer_price / Decimal(100)))
            else:
                return self.selling_price
        else:
            if self.is_offer_valid:
                min_variation_price = self.get_product_variation.all().aggregate(Min('selling_price'))
                return min_variation_price['selling_price__min'] - (
                            min_variation_price['selling_price__min'] * (self.offer_price / Decimal(100)))
            else:
                min_variation_price = self.get_product_variation.all().aggregate(Min('selling_price'))
                return min_variation_price['selling_price__min']

    def multi_price(self):
        if not self.get_product_variation.exists():
            if self.is_offer_valid:
                return '৳' + str(self.selling_price - (self.selling_price * (self.offer_price / Decimal(100))))
            else:
                return None
        else:
            all_variation = self.get_product_variation.all()
            minprice = all_variation.aggregate(Min('selling_price'))
            maxprice = all_variation.aggregate(Max('selling_price'))
            if self.is_offer_valid:
                return '৳' + str(Decimal(minprice['selling_price__min']) - (
                        Decimal(minprice['selling_price__min']) * (
                        self.offer_price / Decimal(100)))) + ' - ' + '৳' + str(
                    Decimal(maxprice['selling_price__max']) - (
                            Decimal(maxprice['selling_price__max']) * (self.offer_price / Decimal(100))))
            else:
                return '৳' + str(minprice['selling_price__min']) + ' - ' + '৳' + str(maxprice['selling_price__max'])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE,
                                related_name="get_product_image")
    display = models.BooleanField(default=False)
    image = models.ImageField()
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ProductOption(models.Model):
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE, related_name="get_product_option")
    option = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name="get_option_of_product")
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ProductVariance(models.Model):
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE, related_name="get_product_variation")
    variance = models.ForeignKey(ProductVariationAdmin, on_delete=models.SET_NULL, null=True,
                                 related_name="get_variation_of_product")
    color = models.CharField(max_length=75, null=True, blank=True)
    color_description = models.CharField(max_length=150, null=True, blank=True)
    size = models.CharField(max_length=75, null=True, blank=True)
    size_description = models.CharField(max_length=150, null=True, blank=True)
    style = models.CharField(max_length=75, null=True, blank=True)
    style_description = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField()
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
