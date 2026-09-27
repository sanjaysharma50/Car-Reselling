from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from cars.views import (
    home,
    brands,
    brand_cars,
    car_detail,
    sell_car,
    register,
    user_login,
    user_logout,
    profile,
)


urlpatterns = [

    # =========================
    # ADMIN
    # =========================

    path(
        'admin/',
        admin.site.urls
    ),


    # =========================
    # ROOT -> LOGIN
    # =========================

    path(
        '',
        user_login,
        name='login'
    ),


    # =========================
    # HOME
    # =========================

    path(
        'home/',
        home,
        name='home'
    ),


    # =========================
    # BRANDS
    # =========================

    path(
        'brands/',
        brands,
        name='brands'
    ),


    # =========================
    # BRAND CARS
    # =========================

    path(
        'brands/<str:brand>/',
        brand_cars,
        name='brand_cars'
    ),


    # =========================
    # CAR DETAIL
    # =========================

    path(
        'car/<int:id>/',
        car_detail,
        name='car_detail'
    ),


    # =========================
    # REGISTER
    # =========================

    path(
        'register/',
        register,
        name='register'
    ),


    # =========================
    # LOGIN
    # =========================

    path(
        'login/',
        user_login,
        name='login_page'
    ),


    # =========================
    # LOGOUT
    # =========================

    path(
        'logout/',
        user_logout,
        name='logout'
    ),


    # =========================
    # SELL YOUR CAR
    # =========================

    path(
        'sell/',
        sell_car,
        name='sell_car'
    ),


    # =========================
    # PROFILE
    # =========================

    path(
        'profile/',
        profile,
        name='profile'
    ),
]


# =========================
# MEDIA + STATIC
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.BASE_DIR / 'cars' / 'static'
    )
