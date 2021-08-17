from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from admin_app.models import Category
from seller_app.models import ProductImage, Product, ProductOption, Shop, ProductVariance
from seller_app.serializers import ProductImageSerializer, ProductSerializer, ProductMinSerializer
from user_app.models import Cart, CartProduct, UserLocation, CheckoutProduct, Checkout


class FrontProductMiniSerializer(serializers.ModelSerializer):
    get_product_image = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'multi_price',
            'first_price',
            'product_price',
            'selling_price',
            'quantity',
            'offer_price',
            'offer_price_start',
            'offer_price_end',
            'get_product_image',
        ]


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ('id', 'name',)


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariance
        exclude = ('updated', 'date_joined',)


class ProductShopMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('slug', 'name',)


class FrontSingleProductSerializer(serializers.ModelSerializer):
    get_product_image = ProductImageSerializer(many=True)
    # get_product_option = ProductOptionSerializer(many=True)
    get_product_variation = ProductVariationSerializer(many=True)
    shop = ProductShopMiniSerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'shop',
            'product_price',
            'selling_price',
            'quantity',
            'description',
            'offer_price',
            'offer_price_start',
            'offer_price_end',
            'multi_price',
            'get_product_image',
            'get_product_variation',
        ]
        # exclude = ('updated', 'date_joined', 'trash', 'active')


class CartProductSerializer(serializers.ModelSerializer):
    variation = ProductVariationSerializer(allow_null=True)
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = "__all__"


class CartProductSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = "__all__"


class ShopFrontSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    get_product_shop = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'contact_number', 'slug', 'banner', 'business_location', 'get_product_shop']


class CategorySerializer(serializers.ModelSerializer):
    child = serializers.ListSerializer(source="subcategory", required=False, child=RecursiveField(),
                                       read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'slug','name', 'child',)


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = "__all__"


class CheckoutSerializer(serializers.ModelSerializer):
    location = UserLocationSerializer()

    class Meta:
        model = Checkout
        fields = "__all__"


class CheckoutProductSerializer(serializers.ModelSerializer):
    product = ProductMinSerializer()
    checkout = CheckoutSerializer()

    class Meta:
        model = CheckoutProduct
        fields = "__all__"


class OrderMinProductSerializer(serializers.ModelSerializer):
    get_product_image = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'get_product_image']


class ChoicesSerializerField(serializers.SerializerMethodField):
    """
    A read-only field that return the representation of a model field with choices.
    """

    def to_representation(self, value):
        # sample: 'get_XXXX_display'
        method_name = 'get_{field_name}_display'.format(field_name=self.field_name)
        # retrieve instance method
        method = getattr(value, method_name)
        # finally use instance method to return result of get_XXXX_display()
        return method()


class UserCheckoutProduct(serializers.ModelSerializer):
    status_choices = (
        (0, 'Order placed'),
        (1, 'Processing'),
        (2, 'Packaging'),
        (3, 'On-way'),
        (4, 'Reached'),
        (5, 'Completed'),
    )
    product = OrderMinProductSerializer()
    status = ChoicesSerializerField()

    class Meta:
        model = CheckoutProduct
        fields = [
            'id',
            'checkout',
            'product',
            'selling_price',
            'offer_price',
            'quantity',
            'status',
        ]


class UserCheckout(serializers.ModelSerializer):
    checkout_products = UserCheckoutProduct(many=True)

    class Meta:
        model = Checkout
        fields = [
            'checkout_products',
            'slug',
            'total_price',
            'location',
            'completed',
        ]
