from django.contrib import admin

from .models import (
    Car,
    CarImage,
    SellRequest,
    ContactRequest,
)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'brand',
        'model',
        'year',
        'price',
        'fuel',
        'transmission',
        'city',
        'status',
        'is_featured',
        'created_at',
    )

    list_filter = (
        'brand',
        'fuel',
        'transmission',
        'city',
        'status',
        'is_featured',
    )

    search_fields = (
        'brand',
        'model',
        'city',
        'seller_name',
        'seller_phone',
    )

    list_editable = (
        'status',
        'is_featured',
    )

    ordering = (
        '-created_at',
    )


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):

    list_display = (
        'car',
        'image',
    )

    search_fields = (
        'car__brand',
        'car__model',
    )


@admin.register(SellRequest)
class SellRequestAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'phone',
        'brand',
        'model',
        'year',
        'city',
        'expected_price',
        'created_at',
    )

    list_filter = (
        'city',
        'year',
        'created_at',
    )

    search_fields = (
        'name',
        'phone',
        'email',
        'brand',
        'model',
        'city',
    )

    ordering = (
        '-created_at',
    )


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'phone',
        'car',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'name',
        'phone',
        'email',
        'car__brand',
        'car__model',
    )

    ordering = (
        '-created_at',
    )