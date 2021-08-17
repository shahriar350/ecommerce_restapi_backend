from django.urls import path
from . import views

urlpatterns = [
    path('seller/request/', views.seller_request),
    path('seller/login/', views.seller_login),
    path('user/', views.get_user),
    path('logout/', views.logout_now),
    path('mytoken/', views.login_set_cookie),
]
