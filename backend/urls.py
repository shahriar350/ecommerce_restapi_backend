import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/auth/', include('auth_app.urls')),
                  path('api/seller/', include('seller_app.urls')),
                  path('api/nonuser/', include('non_user_app.urls')),
                  path('api/user/', include('user_app.urls')),
                  path('__debug__/', include(debug_toolbar.urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
