from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from admin_app.models import ShopCategory
from seller_app.models import Shop, ProductVariance, Product, ProductImage, ProductOption


class ShopCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'contact_number', 'slug', 'banner', 'business_location']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.business_location = validated_data.get('business_location', instance.business_location)
        if validated_data.get('banner') is not None:
            instance.banner = validated_data.get('banner', instance.banner)
        instance.save()
        return instance


class PostSellerShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"

    def validate_contact_number(self, data):
        if data is not None:
            if Shop.objects.filter(contact_number=data).count() > 0:
                raise ValidationError('Contact number is already taken')
            elif not data.isdecimal():
                raise serializers.ValidationError("Phone number must be in number format")
            elif len(data) != 11:
                raise serializers.ValidationError("Phone number must be 11 digit")
            return data


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'display')


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = "__all__"


class ProductVarianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariance
        fields = "__all__"


class ProductImageVarianceSerializer(serializers.ModelSerializer):
    get_product_image = ProductImageSerializer(many=True, read_only=True)
    get_product_variation = ProductVarianceSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'product_price',
            'selling_price',
            'quantity',
            'active',
            'description',
            'offer_price',
            'offer_price_start',
            'offer_price_end',
            'next_stock_date',
            'get_product_image',
            'get_product_variation'
        )


class ProductSerializer(serializers.ModelSerializer):
    get_product_image = ProductImageSerializer(many=True, read_only=True)
    get_product_variation = ProductVarianceSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'brand',
            'product_price',
            'selling_price',
            'quantity',
            'active',
            'description',
            'offer_price',
            'offer_price_start',
            'offer_price_end',
            'next_stock_date',
            'get_product_image',
            'get_product_variation'
        )


class ProductMinSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=150)
    slug = serializers.SlugField()
    product_price = serializers.CharField(max_length=150)
    selling_price = serializers.CharField(max_length=150)
    quantity = serializers.CharField(max_length=150)


