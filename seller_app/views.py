import datetime
import json
from decimal import Decimal

import ujson
from django.db.models import F, Count, Sum
from django.db.models.functions import TruncDay
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from admin_app.models import ProductVariationAdmin, Brand
from admin_app.serializers import CategorySerializer, ProductVariationAdminSerializer, BrandSerializer
from auth_app.models import Users
from backend.mixins import PageNumberPaginationWithCount
from seller_app.models import Shop, Product, ProductImage
from seller_app.serializers import PostSellerShopSerializer, ShopSerializer, ProductSerializer, ProductImageSerializer, \
    ProductOptionSerializer, ProductVarianceSerializer, ProductMinSerializer
from user_app.models import Checkout, CheckoutProduct
from user_app.serializers import CheckoutProductSerializer


@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
def single_shop(request, id=None):
    if request.method == 'PUT':
        # update information
        instance = Shop.objects.get(pk=id, trash=False, active=True)
        serializer = ShopSerializer(instance,
                                    data={
                                        'name': request.data.get('name'),
                                        'business_location': request.data.get('business_location'),
                                        'banner': request.FILES.get('banner', None),
                                    }, partial=True
                                    )
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        if serializer.validated_data.get('banner') is not None:
            return Response(data=ShopSerializer(data, context={"request": request}).data.get('banner'),
                            status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'PATCH':
        # soft delete shop
        instance = Shop.objects.get(pk=id, trash=False, active=True)
        instance.active = False
        instance.trash = True
        instance.save()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        # hard delete shop
        instance = Shop.objects.get(pk=id, trash=True)
        instance.delete()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # restore shop
        instance = Shop.objects.filter(trash=True).get(pk=id)
        instance.active = True
        instance.trash = False
        instance.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def shop_action(request):
    if request.method == 'POST':
        serializer = PostSellerShopSerializer(
            data={
                'category': request.data.get('category'),
                'name': request.data.get('name'),
                'contact_number': request.data.get('contact_number'),
                'business_location': request.data.get('business_location'),
                'banner': request.FILES.get('banner'),
                'seller': request.user.id
            }
        )
        serializer.is_valid(raise_exception=True)
        shop = serializer.save()
        if shop:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    else:
        shops = Shop.objects.filter(seller=request.user)
        active_shops = shops.filter(active=True)
        non_active_shops = shops.filter(active=False, trash=False)
        delete_shops = shops.filter(trash=True)
        return JsonResponse(
            {
                'active_shops': ShopSerializer(active_shops, many=True, context={"request": request}).data,
                'non_active_shops': ShopSerializer(non_active_shops, many=True, context={"request": request}).data,
                'delete_shops': ShopSerializer(delete_shops, many=True, context={"request": request}).data
            }, status=status.HTTP_200_OK)


@api_view(['GET'])
def checkshopslug(request, slug):
    try:
        shop = Shop.objects.filter(seller=request.user, active=True, trash=False).get(slug=slug)
        shop_cat = shop.category.get_category.all()
        brands = Brand.objects.filter(shop=shop.category)
        print(brands)
        variation = ProductVariationAdmin.objects.all()
        return JsonResponse({
            'shop': ShopSerializer(shop).data.get('id'),
            'pro_cat': CategorySerializer(shop_cat, many=True).data,
            'variations': ProductVariationAdminSerializer(variation, many=True).data,
            'brands': BrandSerializer(brands, many=True).data
        }, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def product_variation(request):
    data = ProductVariationAdmin.objects.all()
    return Response(data=ProductVariationAdminSerializer(data, many=True).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def seller_shop_all(request):
    shops = Shop.objects.filter(seller=request.user, active=True, trash=False)
    return Response(data=ShopSerializer(shops, many=True).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def new_product(request, shop_id=None):
    # get_shop
    shop = Shop.objects.get(pk=shop_id)
    basic = ujson.loads(request.data.getlist('basic')[0])
    # product serializer
    product_serializer = ProductSerializer(data=basic)
    product_serializer.is_valid(raise_exception=True)
    product = product_serializer.save(shop=shop, seller=request.user)
    # print(product_serializer.data)
    if product:
        try:
            # product image start
            product_images = []
            for i in request.FILES.getlist('images'):
                product_images.append({'image': i})

            product_image_serializer = ProductImageSerializer(data=product_images, many=True)
            product_image_serializer.is_valid(raise_exception=True)
            product_image_serializer.save(product=product)

            # primary image upload
            primary_image = []
            for i in request.FILES.getlist('primary_image'):
                primary_image.append({'image': i})

            primary_image = ProductImageSerializer(data=primary_image, many=True)

            primary_image.is_valid(raise_exception=True)

            primary_image.save(display=True, product=product)

            # product image end
            # category set
            product_options = []
            for i in request.data.getlist('category'):
                product_options.append({'option': i})
            product_option_serializer = ProductOptionSerializer(data=product_options, many=True)

            product_option_serializer.is_valid(raise_exception=True)
            product_option_serializer.save(product=product)
            # variation serializer
            if request.data.get('variance'):
                variances = ujson.loads(request.data.getlist('variance')[0])
                for index, val in enumerate(variances):
                    val['image'] = request.FILES.getlist('variance_images')[index]

                product_variation_serializer = ProductVarianceSerializer(data=variances, many=True)
                product_variation_serializer.is_valid(raise_exception=True)

                product_variation_serializer.save(product=product)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            product.delete()
            return Response(status=status.HTTP_403_FORBIDDEN, data=e)


class SmallCursorPagination(PageNumberPaginationWithCount):
    page_size = 5


class ProductAllView(ListAPIView):
    serializer_class = ProductMinSerializer
    pagination_class = SmallCursorPagination

    def get_queryset(self):
        products = Product.objects.filter(seller=self.request.user, active=True, trash=False)
        return products


@api_view(['GET'])
def inactivate_product(request):
    inactivate_products = Product.objects.filter(seller=request.user, active=False)
    trash_products = Product.objects.filter(seller=request.user, trash=True)
    return Response(data={
        'inactivate_products': ProductSerializer(inactivate_products, many=True).data,
        'trash_products': ProductSerializer(trash_products, many=True).data,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def dash_basic_info(request):
    # products = Product.objects.filter(seller=request.user, trash=False, active=True).count()
    shops = Shop.objects.filter(seller=request.user, trash=False, active=True).count()
    seller_products = Product.objects.filter(seller=request.user, trash=False, active=True)
    checkout_seller_products = CheckoutProduct.objects.filter(product__in=seller_products)
    today_earning = Decimal(0)
    total_price = Decimal(0)
    for i in checkout_seller_products:
        total_price += (i.selling_price - (i.selling_price * (i.offer_price / Decimal(100)))) * i.quantity

        if i.created.date() == datetime.datetime.today().date():
            today_earning += (i.selling_price - (i.selling_price * (i.offer_price / Decimal(100)))) * i.quantity
    return Response(data={
        'products': seller_products.count(),
        'shops': shops,
        'total_selling_price': total_price,
        'today_selling_price': today_earning
    }, status=status.HTTP_200_OK)


# edit area start
@api_view(['GET'])
def basic_edit_product(request, product_slug=None):
    if product_slug is not None:
        products = ProductSerializer(
            Product.objects.filter(seller=request.user).prefetch_related('get_product_image',
                                                                         'get_product_variation').get(
                slug=product_slug),
            context={'request': request})
        return Response(data={
            'product': products.data,
        }, status=status.HTTP_200_OK)


# edit area end
#
@api_view(['POST'])
def edit_image_product(request, product_slug=None):
    if product_slug is not None:
        product = Product.objects.filter(seller=request.user).get(slug=product_slug)
        if product.get_product_image.count() < 6:
            product_images = []
            for i in request.FILES.getlist('image'):
                if request.POST.get('display'):
                    product_images.append({'image': i, 'display': True})
                else:
                    product_images.append({'image': i})
            images = ProductImageSerializer(data=product_images, many=True)
            images.is_valid(raise_exception=True)
            if request.POST.get('display'):
                product_image_up = product.get_product_image.all()
                product_image_up.update(display=False)
                images_save = images.save(product=product)
            else:
                images_save = images.save(product=product)
            return Response(
                data={'image': ProductImageSerializer(images_save, context={'request': request}, many=True).data},
                status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['DELETE'])
def delete_image_product(request, shop_slug=None, image_id=None):
    if shop_slug is not None:
        product_images = Product.objects.filter(seller=request.user).get(slug=shop_slug,
                                                                         seller=request.user).get_product_image.all()
        image = product_images.get(pk=image_id)
        if image:
            image.delete()
            return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
def edit_basic(request, product_id=None):
    if product_id is not None:
        product = Product.objects.get(pk=product_id, seller=request.user)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
def product_softdelete(request, product_id=None):
    if product_id is not None:
        product = Product.objects.get(pk=product_id, seller=request.user)
        product.trash = True
        product.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def product_delete(request, product_id=None):
    if product_id is not None:
        product = Product.objects.get(pk=product_id, seller=request.user)
        product.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
def product_softdelete_restore(request, product_id=None):
    if product_id is not None:
        product = Product.objects.get(pk=product_id, seller=request.user)
        product.trash = False
        product.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
def update_as_default_image(request, product_id=None, image_id=None):
    if image_id is not None and product_id is not None:
        update_product_image = Product.objects.prefetch_related('get_product_image').get(pk=product_id,
                                                                                         seller=request.user)
        update_product_image.get_product_image.all().update(display=False)
        update_product_image.get_product_image.filter(pk=image_id).update(display=True)
        return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
def update_variance(request, product_id=None, variance_id=None):
    if product_id is not None and variance_id is not None:
        product_get_variance = Product.objects.get(pk=product_id, seller=request.user).get_product_variation.get(
            pk=variance_id)
        if product_get_variance is not None:
            product_va = ProductVarianceSerializer(product_get_variance, data=request.data, partial=True)

            product_va.is_valid(raise_exception=True)
            if request.FILES.get('image'):
                product_va.save(image=request.FILES.get('image'))
            else:
                product_va.save()
            return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def new_product_variation(request, product_id=None):
    product = Product.objects.get(pk=product_id, seller=request.user)
    variances = ujson.loads(request.data.getlist('variance')[0])
    for index, val in enumerate(variances):
        val['image'] = request.FILES.getlist('variance_images')[index]

    product_variation_serializer = ProductVarianceSerializer(data=variances, many=True, context={'request': request})
    product_variation_serializer.is_valid(raise_exception=True)
    product_variation_serializer.save(product=product)
    return Response(status=status.HTTP_201_CREATED, data=product_variation_serializer.data)


@api_view(['DELETE'])
def remove_variance(request, product_id=None, variance_id=None):
    product_varia = Product.objects.get(seller=request.user, pk=product_id).get_product_variation.get(pk=variance_id)
    product_varia.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def seller_orders(request):
    checkout_products = CheckoutProduct.objects.select_related('checkout__location').filter(
        product__seller=request.user, received=False).order_by(
        'created')

    return Response(data=CheckoutProductSerializer(checkout_products, many=True).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_status(request, checkout_product_id=None):
    if checkout_product_id is not None and request.data.get('order_status') < 5:
        checkout_product_status = CheckoutProduct.objects.get(pk=checkout_product_id)
        checkout_product_status.status = request.data.get('order_status')
        checkout_product_status.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_502_BAD_GATEWAY)


@api_view(['GET'])
def seller_total_earning(request):
    seller_products = Product.objects.filter(seller=request.user)
    checkout_seller_products = CheckoutProduct.objects.filter(product__in=seller_products)
    today_earning = Decimal(0)
    total_price = Decimal(0)
    for i in checkout_seller_products:
        total_price += (i.selling_price - (i.selling_price * (i.offer_price / Decimal(100)))) * i.quantity

        if i.created.date() == datetime.datetime.today().date():
            today_earning += (i.selling_price - (i.selling_price * (i.offer_price / Decimal(100)))) * i.quantity
    return Response(status=status.HTTP_200_OK, data={
        'total_selling_price': total_price,
        'today_selling_price': today_earning
    })


@api_view(['GET'])
def chart_sell_vs_date(request):
    seller_products = Product.objects.filter(seller=request.user)
    checkout_product = list(CheckoutProduct.objects.filter(product__in=seller_products,
                                                           created__lte=datetime.datetime.today(),
                                                           created__gt=datetime.datetime.today() - datetime.timedelta(
                                                               days=30)).annotate(
        date=TruncDay('created')).values('date').annotate(total=Count('product')))
    data = [
        ['Date', 'total sale']
    ]
    for d in (datetime.datetime.today() - datetime.timedelta(days=x) for x in range(0, 31)):
        # data.append({str(d.date()): 0})
        avail = [i for i in checkout_product if i['date'].date() == d.date()]
        if len(avail) > 0:
            data.append([d.date().strftime('%d.%m.%Y'), avail[0]['total']])
        else:
            data.append([d.date().strftime('%d.%m.%Y'), 0])
    return Response(data=data, status=status.HTTP_200_OK)


