from rest_framework import serializers

from admin_app.models import Category, ProductVariationAdmin, Brand


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductVariationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariationAdmin
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name','shop']
