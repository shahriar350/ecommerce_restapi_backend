from django.urls import path
from . import views

urlpatterns = [
    path('shop/categories/all/', views.get_shopcategory),
    path('shop/category/filter/<slug:shop_category_slug>/all/', views.category_by_shop_cat),
    path('shop/product/filter/<int:category_id>/', views.filter_product_category),
    path('shop/product/<slug:category_slug>/all/', views.product_by_category),
]
