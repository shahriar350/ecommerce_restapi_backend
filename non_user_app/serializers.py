from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from admin_app.models import ShopCategory, Category
from seller_app.models import Shop, Product, ProductImage, ProductOption
from user_app.serializers import CategorySerializer


class ProductImageInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductInitSerializer(serializers.ModelSerializer):
    get_product_image = ProductImageInitSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'slug', 'name', 'get_product_image',
                  'product_price',
                  'quantity',
                  'offer_price',
                  'offer_price_start',
                  'offer_price_end',
                  'price',
                  'first_price'
                  )


class ShopIntSerializer(serializers.ModelSerializer):
    get_product_shop = ProductInitSerializer(many=True)

    class Meta:
        model = Shop
        fields = (
            'name',
            'slug',
            'get_product_shop',
        )


class getProductByShopCategory(serializers.ModelSerializer):
    get_shop = ShopIntSerializer(many=True)

    class Meta:
        model = ShopCategory
        fields = (
            'id',
            'name',
            'slug',
            'image',
            'get_shop'
        )


class CategorySerializerByShop(serializers.ModelSerializer):
    child = serializers.ListSerializer(source="subcategory", required=False, child=RecursiveField(),
                                       read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'child']


class getProductByShopCategoryWithSub(serializers.ModelSerializer):
    get_category = CategorySerializerByShop(many=True)

    class Meta:
        model = ShopCategory
        fields = (
            'id',
            'name',
            'slug',
            'get_category'
        )


class NonUserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategory',)


# product filter serializer
class ProductOptionFilter(serializers.ModelSerializer):
    product = ProductInitSerializer()

    class Meta:
        model = ProductOption
        fields = [
            'id',
            'product',
            'option',
        ]


class CategoryFilterSerializerByShop(serializers.ModelSerializer):
    # child = serializers.ListSerializer(source="subcategory", required=False, child=RecursiveField(),
    #                                    read_only=True)
    get_option_of_product = ProductOptionFilter(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'get_option_of_product']
