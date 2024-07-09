from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Chere Water API",
      default_version='v1',
      description="This is chere water project",
      contact=openapi.Contact(email="xoliqberdiyevbehruz12@gmail.com"),
      license=openapi.License(name="demo license"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path('admin/', admin.site.urls),
    path('api/v1/admin/common/', include('common.urls')),
    path('api/v1/landing/common/', include('common.landing.urls')),
    path('api/v1/admin/common/', include('common.urls')),
    path('api/v1/admin/orders/', include('order.urls')),
    path('api/v1/landing/products/', include('products.landing.urls')),
    path('api/v1/admin/products/', include('products.urls')),
    path('api/v1/admin/users/', include('users.urls')),
    path('api/v1/landing/users/', include('users.landing.urls')),

    # packages
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
