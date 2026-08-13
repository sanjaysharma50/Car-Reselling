from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Car, ContactRequest, SellRequest


def home(request):

    search = request.GET.get('search', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    fuel = request.GET.get('fuel', '')
    transmission = request.GET.get('transmission', '')
    year = request.GET.get('year', '')
    city = request.GET.get('city', '')
    sort = request.GET.get('sort', '')

    # =========================================
    # AVAILABLE CARS
    # =========================================

    cars = Car.objects.filter(
        status='available'
    )

    # =========================================
    # FEATURED CARS
    # =========================================

    featured_cars = Car.objects.filter(
        status='available',
        is_featured=True
    )[:4]

    # =========================================
    # SEARCH
    # =========================================

    if search:

        cars = cars.filter(
            brand__icontains=search
        ) | cars.filter(
            model__icontains=search
        )

    # =========================================
    # MINIMUM PRICE
    # =========================================

    if min_price:

        cars = cars.filter(
            price__gte=min_price
        )

    # =========================================
    # MAXIMUM PRICE
    # =========================================

    if max_price:

        cars = cars.filter(
            price__lte=max_price
        )

    # =========================================
    # FUEL
    # =========================================

    if fuel:

        cars = cars.filter(
            fuel__iexact=fuel
        )

    # =========================================
    # TRANSMISSION
    # =========================================

    if transmission:

        cars = cars.filter(
            transmission__iexact=transmission
        )

    # =========================================
    # YEAR
    # =========================================

    if year:

        cars = cars.filter(
            year=year
        )

    # =========================================
    # CITY
    # =========================================

    if city:

        cars = cars.filter(
            city__iexact=city
        )

    # =========================================
    # SORT
    # =========================================

    if sort == 'price_low':

        cars = cars.order_by('price')

    elif sort == 'price_high':

        cars = cars.order_by('-price')

    elif sort == 'newest':

        cars = cars.order_by('-created_at')

    elif sort == 'oldest':

        cars = cars.order_by('created_at')

    # =========================================
    # PAGINATION
    # =========================================

    paginator = Paginator(
        cars,
        6
    )

    page_number = request.GET.get('page')

    cars = paginator.get_page(
        page_number
    )

    # =========================================
    # HOME PAGE
    # =========================================

    return render(
        request,
        'cars/home.html',
        {
            'cars': cars,

            'featured_cars': featured_cars,

            'search': search,

            'min_price': min_price,

            'max_price': max_price,

            'fuel': fuel,

            'transmission': transmission,

            'year': year,

            'city': city,

            'sort': sort,

            'paginator': paginator,
        }
    )


# =============================================
# CAR DETAIL
# =============================================

def car_detail(request, id):

    car = get_object_or_404(
        Car,
        id=id
    )

    contact_success = False

    # =========================================
    # CONTACT SELLER
    # =========================================

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        message = request.POST.get(
            'message',
            ''
        ).strip()

        # SAVE CONTACT REQUEST

        if name and phone:

            ContactRequest.objects.create(

                car=car,

                name=name,

                phone=phone,

                email=email,

                message=message
            )

            contact_success = True

    return render(
        request,
        'cars/detail.html',
        {
            'car': car,

            'contact_success': contact_success,
        }
    )


# =============================================
# SELL YOUR CAR
# =============================================

def sell_car(request):

    sell_success = False

    # =========================================
    # SELL FORM
    # =========================================

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        brand = request.POST.get(
            'brand',
            ''
        ).strip()

        model = request.POST.get(
            'model',
            ''
        ).strip()

        year = request.POST.get(
            'year',
            ''
        ).strip()

        kilometers = request.POST.get(
            'kilometers',
            ''
        ).strip()

        city = request.POST.get(
            'city',
            ''
        ).strip()

        expected_price = request.POST.get(
            'expected_price',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        # =====================================
        # SAVE SELL REQUEST
        # =====================================

        if (
            name
            and phone
            and brand
            and model
            and year
            and kilometers
            and city
            and expected_price
        ):

            SellRequest.objects.create(

                name=name,

                phone=phone,

                email=email,

                brand=brand,

                model=model,

                year=year,

                kilometers=kilometers,

                city=city,

                expected_price=expected_price,

                description=description
            )

            sell_success = True

    return render(
        request,
        'cars/sell.html',
        {
            'sell_success': sell_success,
        }
    )