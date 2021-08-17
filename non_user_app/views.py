from django.db.models import Prefetch
# Create your views here.
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response

from admin_app.models import ShopCategory, Category
from non_user_app.serializers import getProductByShopCategory, CategorySerializerByShop, CategoryFilterSerializerByShop, ProductOptionFilter
from seller_app.models import ProductImage, ProductOption, Product
from seller_app.serializers import ShopCategorySerializer
from user_app.serializers import CategorySerializer, FrontProductMiniSerializer


@api_view(['GET'])
def get_shopcategory(request):
    serializer = ShopCategorySerializer(ShopCategory.objects.all(), many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def product_by_category(request, category_slug=None):
    all_cat = Category.objects.filter(shop__slug=category_slug).values_list('id', flat=True)
    products = Product.objects.prefetch_related(Prefetch("get_product_image",
                                                         queryset=ProductImage.objects.filter(
                                                             display=True))).filter(
        get_product_option__option_id__in=all_cat)
    return Response(FrontProductMiniSerializer(products, context={'request': request}, many=True).data)


@api_view(['GET'])
def filter_product_category(request, category_id=None):
    if category_id is not None:
        products = Product.objects.prefetch_related(Prefetch("get_product_image",
                                                             queryset=ProductImage.objects.filter(
                                                                 display=True))).filter(
            get_product_option__option_id=category_id)

        return Response(FrontProductMiniSerializer(products, context={'request': request}, many=True).data)


@api_view(['GET'])
def category_by_shop_cat(request, shop_category_slug=None):
    categories = Category.objects.prefetch_related('subcategory').filter(shop__slug=shop_category_slug, parent=None)
    return Response(CategorySerializer(categories, many=True).data)
