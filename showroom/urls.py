from django.urls import path, include
from rest_framework.routers import DefaultRouter
from showroom import views

app_name = 'showroom'
router = DefaultRouter(trailing_slash=False)
router.register(r'cars', views.CarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]