import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from auth_app.models import Users
from backend.mixins import create_slug
from seller_app.models import Product, ProductVariance


class Cart(models.Model):
    slug = models.SlugField(null=True)
    user = models.ForeignKey(Users, blank=True, null=True, on_delete=models.CASCADE, related_name='user_cart')
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.slug)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE, related_name='user_cart')
    variation = models.ForeignKey(ProductVariance, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='cart_product_variations')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return self.product


class UserLocation(models.Model):
    user = models.ForeignKey(Users, blank=True, on_delete=models.CASCADE, related_name='user_locations')
    area = models.CharField(max_length=150, null=True, blank=True)
    street = models.CharField(max_length=150, null=True, blank=True)
    house = models.CharField(max_length=150, null=True, blank=True)
    post_office = models.CharField(max_length=150, null=True, blank=True)
    post_code = models.CharField(max_length=10, null=True, blank=True)
    police_station = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.post_office + ' ' + self.city


class Checkout(models.Model):
    slug = models.SlugField(editable=False)
    user = models.ForeignKey(Users, blank=True, on_delete=models.CASCADE, related_name='user_checkouts')
    cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE, related_name='cart_checkout')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    location = models.ForeignKey(UserLocation, on_delete=models.CASCADE, related_name="location_checkouts")
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self, uuid.uuid4())
        super().save(*args, **kwargs)


class CheckoutProduct(models.Model):
    status_choices = (
        (0, 'Order placed'),
        (1, 'Processing'),
        (2, 'Packaging'),
        (3, 'On-way'),
        (4, 'Reached'),
        (5, 'Completed'),
    )
    slug = models.SlugField(editable=False)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='checkout_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_checkouts')
    selling_price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
    offer_price = models.PositiveIntegerField(blank=True, default=0,
                                              validators=[MinValueValidator(0), MaxValueValidator(100)])
    quantity = models.PositiveIntegerField(default=1, blank=True, validators=[MinValueValidator(1)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    received = models.BooleanField(default=False)
    status = models.PositiveSmallIntegerField(default=0, choices=status_choices)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self, uuid.uuid4())
        super().save(*args, **kwargs)
