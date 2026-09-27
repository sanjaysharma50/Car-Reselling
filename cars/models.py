from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
    ]

    brand = models.CharField(
        max_length=100
    )

    model = models.CharField(
        max_length=100
    )

    year = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    fuel = models.CharField(
        max_length=50
    )

    transmission = models.CharField(
        max_length=50
    )

    kilometers = models.PositiveIntegerField()

    city = models.CharField(
        max_length=100
    )

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    is_featured = models.BooleanField(
        default=False
    )

    seller_name = models.CharField(
        max_length=100,
        blank=True
    )

    seller_phone = models.CharField(
        max_length=20,
        blank=True
    )

    seller_email = models.EmailField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.brand} {self.model}"


class CarImage(models.Model):

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='cars/'
    )

    def __str__(self):

        return f"{self.car.brand} {self.car.model} Image"


class SellRequest(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sell_requests'
    )

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True
    )

    brand = models.CharField(
        max_length=100
    )

    model = models.CharField(
        max_length=100
    )

    year = models.PositiveIntegerField()

    kilometers = models.PositiveIntegerField()

    city = models.CharField(
        max_length=100
    )

    expected_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.name} - {self.brand} {self.model}"


class ContactRequest(models.Model):

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='contact_requests'
    )

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True
    )

    message = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.name} - {self.car.brand} {self.car.model}"
        