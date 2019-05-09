from django.contrib import admin
from django.urls import path, include
import showroom.urls as car_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_auth.urls')),
    path('api/auth/register', include('rest_auth.registration.urls')),
    path('api/', include(car_urls, namespace='cars')),
]
