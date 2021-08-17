from django.urls import path, include
from . import views

urlpatterns = [
    path('frontend/main/product/', views.frontend_all_product),
    path('frontend/single/product/<int:product_id>/', views.frontend_single_product),
    path('cart/<int:product_id>/', views.cart_product),
    path('cart/remove/<int:product_id>/', views.cart_remove_product),
    path('cart/total/', views.total_cart_count),
    path('cart/all/', views.total_cart),
    path('product/<int:product_id>/<int:variation_id>/', views.product_with_variation),
    path('shop/<slug:shop_slug>/all/product/', views.shop_all_product),
    path('frontend/category/related/', views.main_info_frontend),
    path('register/', views.user_register),
    path('login/', views.user_login),
    path('checkout/total_price/', views.user_checkout_price),
    path('locations/', views.user_location),
    path('checkout/now/', views.user_checkout),
    path('orders/', views.user_orders),
    path('order/product/confirm/<int:checkout_product_id>/', views.confirm_received),
]

