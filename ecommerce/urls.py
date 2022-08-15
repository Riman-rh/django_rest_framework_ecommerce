from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="ecommerce API",
<<<<<<< HEAD
      default_version='v1',
||||||| 1eaf559
=======
       default_version='v1',
>>>>>>> c3f912d0c1f8319141fce352bbd65758aa3a2bfa
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('v3', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
