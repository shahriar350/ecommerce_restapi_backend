from decimal import Decimal

import ujson
from django.contrib.auth import authenticate, login
from django.db.models import Prefetch
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal
from admin_app.models import Category
from auth_app.models import Users
from auth_app.serializers import UserSerializer, SingleUserSerializer
from seller_app.models import Product, ProductImage, ProductVariance, Shop
from seller_app.serializers import ProductSerializer, ProductImageVarianceSerializer
from user_app.models import Cart, CartProduct, UserLocation, CheckoutProduct, Checkout
from user_app.serializers import FrontProductMiniSerializer, FrontSingleProductSerializer, CartProductSerializer, \
    CartSerializer, CartProductSaveSerializer, ShopFrontSerializer, CategorySerializer, UserLocationSerializer, \
    UserCheckout


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(['GET'])
def frontend_all_product(request):
    products = Product.objects.filter(active=True, trash=False).prefetch_related(
        Prefetch("get_product_image", queryset=ProductImage.objects.filter(display=True)))
    products = FrontProductMiniSerializer(products, many=True, context={'request': request})
    return Response(data={
        'products': products.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def frontend_single_product(request, product_id=None):
    if product_id is not None:
        product = Product.objects.select_related('shop').prefetch_related('get_product_variation',
                                                                          'get_product_image').get(pk=product_id)
        serializer = FrontSingleProductSerializer(product, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def cart_product(request, product_id=None):
    if product_id is not None:
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user, active=True)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=request.user, active=True)

            product = Product.objects.get(pk=product_id)
            cart_pro_check = None

            if cart.cart_products.exists():
                cart_pro_check = cart.cart_products.filter(product=product, product__active=True,
                                                           product__trash=False).first()

            if product:
                variation = None
                if request.data.get('variation') is not None:
                    variation = ProductVariance.objects.get(pk=request.data.get('variation'))
                if cart_pro_check is None:
                    # new cart product
                    cart_product_serializer = CartProductSaveSerializer(data={
                        'cart': cart.pk,
                        'product': product.pk,
                        'variation': variation if variation is None else variation.pk,
                        'quantity': request.data.get('quantity'),
                    })
                    cart_product_serializer.is_valid(raise_exception=True)
                    cart_product_serializer.save()
                    return Response(status=status.HTTP_201_CREATED, data=cart_product_serializer.data)

                else:
                    # update cart product with quantity
                    cart_product_update_serializer = CartProductSaveSerializer(cart_pro_check, data={
                        'variation': variation if variation is None else variation.pk,
                        'quantity': request.data.get('quantity'),
                    }, partial=True)
                    cart_product_update_serializer.is_valid(raise_exception=True)
                    cart_product_update_serializer.save()
                    return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def total_cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(user=request.user, active=True, cart_products__product__active=True,
                                       cart_products__product__trash=False).first().cart_products.count()
            return Response(data=cart, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=0, status=status.HTTP_200_OK)
    else:
        return Response(data=request.session['my_cart'], status=status.HTTP_200_OK)


@api_view(['GET'])
def total_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.prefetch_related('cart_products', 'cart_products__product',
                                             'cart_products__variation',
                                             Prefetch("cart_products__product__get_product_image",
                                                      queryset=ProductImage.objects.filter(display=True))).filter(
            user=request.user, active=True, cart_products__product__active=True,
            cart_products__product__trash=False).first()
        return Response(data=CartSerializer(cart, context={'request': request}).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def product_with_variation(request, product_id=None, variation_id=None):
    if product_id is not None:
        if variation_id > 0:
            product = Product.objects.prefetch_related(
                Prefetch('get_product_image', queryset=ProductImage.objects.filter(display=True)),
                Prefetch('get_product_variation', queryset=ProductVariance.objects.filter(pk=variation_id))).get(
                pk=product_id)
        else:
            product = Product.objects.prefetch_related(
                Prefetch('get_product_image', queryset=ProductImage.objects.filter(display=True))).get(
                pk=product_id)
        return Response(data=ProductImageVarianceSerializer(product, context={'request': request}).data,
                        status=status.HTTP_200_OK)


@api_view(['DELETE'])
def cart_remove_product(request, product_id=None):
    if product_id is not None:
        cart = Cart.objects.prefetch_related('cart_products').get(user=request.user, active=True)
        cart.cart_products.get(product=product_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def shop_all_product(request, shop_slug=None):
    if shop_slug is not None:
        my_shop = Shop.objects.prefetch_related(
            Prefetch('get_product_shop__get_product_image', queryset=ProductImage.objects.filter(display=True))).get(
            slug=shop_slug)
        return Response(data=ShopFrontSerializer(my_shop, context={"request": request}).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def main_info_frontend(request):
    category = Category.objects.prefetch_related('subcategory').filter(parent_id=None)
    # print(category)
    return Response(status=status.HTTP_200_OK, data=CategorySerializer(category, many=True).data)


@api_view(['POST'])
def user_register(request):
    user_serializer = UserSerializer(data=request.data)
    user_serializer.is_valid(raise_exception=True)
    user_serializer.save()
    return Response(status=status.HTTP_200_OK, data=user_serializer.data)


@api_view(['POST'])
def user_login(request):
    serializer = SingleUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    number = serializer.validated_data['phone_number']
    password = serializer.validated_data['password']
    user = authenticate(username=number, password=password)
    if user:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    else:
        raise ValidationError('Please provide correct credential')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_checkout_price(request):
    try:
        cart = Cart.objects.prefetch_related('cart_products', 'cart_products__product',
                                             'cart_products__variation').get(
            user=request.user,
            active=True)
        total_price = Decimal(0)
        for cart_pro in cart.cart_products.all():
            price = Decimal(0)
            if cart_pro.variation:
                price = cart_pro.variation.selling_price * cart_pro.quantity
            else:
                price = cart_pro.product.selling_price * cart_pro.quantity
            #     check offer
            if cart_pro.product.is_offer_valid:
                price = price - (price * (cart_pro.product.offer_price / Decimal(100)))
            total_price += price
        return Response(status=status.HTTP_200_OK, data=total_price)
    except Cart.DoesNotExist:
        return Response(data=-1, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_location(request):
    if request.method == 'POST':
        location_serializer = UserLocationSerializer(data=request.data)
        location_serializer.is_valid(raise_exception=True)
        location_serializer.save(user=request.user)
        return Response(data=location_serializer.data['id'], status=status.HTTP_201_CREATED)
    else:
        return Response(
            data=UserLocationSerializer(UserLocation.objects.filter(user=request.user).all(), many=True).data,
            status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_checkout(request):
    if request.method == 'POST':
        cart = Cart.objects.prefetch_related('cart_products', 'cart_products__product').get(user=request.user,
                                                                                            active=True)
        total_price = Decimal(0)
        cart_product_init = []
        for cart_pro in cart.cart_products.all():
            price = Decimal(0)
            offer_price = 0
            if cart_pro.variation:
                price = cart_pro.variation.selling_price * cart_pro.quantity
            else:
                price = cart_pro.product.selling_price * cart_pro.quantity
            #     check offer
            if cart_pro.product.is_offer_valid:
                offer_price = cart_pro.product.offer_price
                price = price - (price * (cart_pro.product.offer_price / Decimal(100)))
            total_price += price

            cart_product_init.append(
                CheckoutProduct(
                    product=cart_pro.product,
                    selling_price=price,
                    offer_price=offer_price,
                    quantity=cart_pro.quantity
                )
            )

        checkout = Checkout(
            user=request.user,
            cart=cart,
            total_price=total_price,
            location=UserLocation.objects.get(pk=request.data.get('location')),
        )
        checkout.save()
        for data in cart_product_init:
            data.checkout = checkout
            data.save()
        cart.active = False
        cart.save()
        return Response(status=status.HTTP_201_CREATED)

    else:
        return Response(
            data=UserLocationSerializer(UserLocation.objects.filter(user=request.user).all(), many=True).data,
            status=status.HTTP_200_OK)


@api_view(['GET'])
def user_orders(request):
    checkout_serializer = UserCheckout(Checkout.objects.prefetch_related('checkout_products', Prefetch(
        'checkout_products__product__get_product_image', queryset=ProductImage.objects.filter(display=True))).order_by(
        '-created').filter(
        user=request.user), many=True, context={'request': request})
    return Response(data=checkout_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def confirm_received(request, checkout_product_id=None):
    if checkout_product_id is not None:
        checkout_product_status = CheckoutProduct.objects.get(pk=checkout_product_id)
        print(checkout_product_status.status)
        if checkout_product_status.status == 4:
            print('asdfsaf')
            checkout_product_status.status = 5
            print(checkout_product_status.status)
            checkout_product_status.save()
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
