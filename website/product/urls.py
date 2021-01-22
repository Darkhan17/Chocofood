from django.urls import path, include, re_path
from rest_framework import routers
from product import views
from django.views.decorators.cache import cache_page


router = routers.DefaultRouter()
router.register('api/Products', views.ProductView)
router.register('api/Shops', views.ShopsView)
urlpatterns = [
    path('',include(router.urls)),
 #path('api/Shops/<str:requestCategory>/<int:product_id>/', views.ProductfromShop)
    path('api/<slug:category>/maxprice', views.maxOfCategory, name='max-category' ),
    path('api/<slug:category>/minprice', views.minOfCategory, name='min-category'),
]

