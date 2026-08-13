from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from cars.views import home, car_detail, sell_car


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        home,
        name='home'
    ),

    path(
        'car/<int:id>/',
        car_detail,
        name='car_detail'
    ),

    path(
        'sell/',
        sell_car,
        name='sell_car'
    ),

]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.BASE_DIR / 'cars' / 'static'
    )