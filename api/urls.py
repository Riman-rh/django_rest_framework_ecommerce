from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.registration),
    path('categoryList/',views.category_list),
    path('productList/', views.product_list),
    path('productCreate/', views.product_create),
    path('productGet/',views.product_get),
    path('productUpdate/',views.product_update),
    path('reviewList/',views.review_list),
    path('reviewCreate/',views.review_create),
    path('reviewUpdate/',views.review_update),
    path('order/',views.orderProcess),
    path('orderComplete/', views.orderComplete)
]