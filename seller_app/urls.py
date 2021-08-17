from django.urls import path
from . import views

urlpatterns = [
    path('shop/action/', views.shop_action),
    path('shop/single/action/<int:id>/', views.single_shop),
    path('shops/all/', views.seller_shop_all),
    path('shop/check/<slug:slug>/', views.checkshopslug),
    path('shop/product/variation/all/', views.product_variation),
    path('product/new/<int:shop_id>/', views.new_product),
    path('product/new/variation/<int:product_id>/', views.new_product_variation),
    path('product/softdelete/<int:product_id>/', views.product_softdelete),
    path('product/delete/<int:product_id>/', views.product_delete),
    path('product/softdelete/restore/<int:product_id>/', views.product_softdelete_restore),
    path('product/all/', views.ProductAllView.as_view()),
    path('product/all/inactivate/', views.inactivate_product),
    path('dashboard/basicinfo/', views.dash_basic_info),
    path('product/edit/<slug:product_slug>/basic/', views.basic_edit_product),
    path('product/edit/<slug:product_slug>/image/', views.edit_image_product),
    path('product/edit/<slug:shop_slug>/<int:image_id>/image/delete/', views.delete_image_product),
    path('product/edit/<int:product_id>/basicupdate/', views.edit_basic),
    path('product/update/default/image/<int:product_id>/<int:image_id>/basicupdate/', views.update_as_default_image),
    path('product/update/variance/<int:product_id>/<int:variance_id>/basicupdate/', views.update_variance),
    path('product/delete/variance/<int:product_id>/<int:variance_id>/', views.remove_variance),
    path('my_orders/', views.seller_orders),
    path('order/product/update/status/<int:checkout_product_id>/',views.update_status),
    path('total_earning/',views.seller_total_earning),
    path('chart/totalsell/date/',views.chart_sell_vs_date),
    # path('order/delivered/<int:checkout_product_id>/', views.order_delivered)
]
