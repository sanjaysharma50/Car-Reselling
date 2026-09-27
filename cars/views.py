from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Car, ContactRequest, SellRequest


# =============================================
# HOME
# =============================================

def home(request):

    search = request.GET.get('search', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    fuel = request.GET.get('fuel', '')
    transmission = request.GET.get('transmission', '')
    year = request.GET.get('year', '')
    city = request.GET.get('city', '')
    sort = request.GET.get('sort', '')

    cars = Car.objects.filter(
        status='available'
    )

    featured_cars = Car.objects.filter(
        status='available',
        is_featured=True
    )[:4]

    # =========================
    # SEARCH
    # =========================

    if search:

        cars = cars.filter(
            brand__icontains=search
        ) | cars.filter(
            model__icontains=search
        )

    # =========================
    # PRICE
    # =========================

    if min_price:
        cars = cars.filter(
            price__gte=min_price
        )

    if max_price:
        cars = cars.filter(
            price__lte=max_price
        )

    # =========================
    # FUEL
    # =========================

    if fuel:
        cars = cars.filter(
            fuel__iexact=fuel
        )

    # =========================
    # TRANSMISSION
    # =========================

    if transmission:
        cars = cars.filter(
            transmission__iexact=transmission
        )

    # =========================
    # YEAR
    # =========================

    if year:
        cars = cars.filter(
            year=year
        )

    # =========================
    # CITY
    # =========================

    if city:
        cars = cars.filter(
            city__iexact=city
        )

    # =========================
    # SORT
    # =========================

    if sort == 'price_low':

        cars = cars.order_by(
            'price'
        )

    elif sort == 'price_high':

        cars = cars.order_by(
            '-price'
        )

    elif sort == 'newest':

        cars = cars.order_by(
            '-created_at'
        )

    elif sort == 'oldest':

        cars = cars.order_by(
            'created_at'
        )

    # =========================
    # PAGINATION
    # =========================

    paginator = Paginator(
        cars,
        6
    )

    page_number = request.GET.get(
        'page'
    )

    cars = paginator.get_page(
        page_number
    )

    # =========================
    # RENDER HOME
    # =========================

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
# BRANDS
# =============================================

def brands(request):

    # Available cars only.
    # Prefetch images so each brand can use the first
    # available car image on the Brands page.
    cars = (
        Car.objects
        .filter(status='available')
        .prefetch_related('images')
        .order_by('brand', '-created_at')
    )

    # Group cars by brand.
    brand_data = {}

    for car in cars:

        if not car.brand:
            continue

        brand = car.brand.strip()

        if not brand:
            continue

        if brand not in brand_data:
            brand_data[brand] = {
                'name': brand,
                'count': 0,
                'image': None,
            }

        brand_data[brand]['count'] += 1

        # Use the first available car image for this brand.
        if brand_data[brand]['image'] is None:
            first_image = car.images.first()

            if first_image:
                brand_data[brand]['image'] = first_image

    # Keep brands alphabetically sorted.
    brand_list = sorted(
        brand_data.values(),
        key=lambda item: item['name'].lower()
    )

    return render(
        request,
        'cars/brands.html',
        {
            'brands': brand_list,
        }
    )


def brand_cars(request, brand):

    cars = Car.objects.filter(
        status='available',
        brand__iexact=brand
    ).order_by('-created_at')

    return render(
        request,
        'cars/brand_cars.html',
        {
            'cars': cars,
            'brand': brand,
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
# REGISTER
# =============================================

def register(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        # =========================
        # USERNAME VALIDATION
        # =========================

        if not username:

            return render(
                request,
                'cars/register.html',
                {
                    'error': 'Username is required.'
                }
            )

        # =========================
        # PASSWORD VALIDATION
        # =========================

        if password != confirm_password:

            return render(
                request,
                'cars/register.html',
                {
                    'error': 'Passwords do not match.'
                }
            )

        # =========================
        # USERNAME EXISTS
        # =========================

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'cars/register.html',
                {
                    'error': 'Username already exists.'
                }
            )

        # =========================
        # CREATE USER
        # =========================

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(
            request,
            user
        )

        # Register successful -> Home
        return redirect(
            '/home/'
        )

    return render(
        request,
        'cars/register.html'
    )


# =============================================
# LOGIN
# =============================================

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        # =========================
        # AUTHENTICATE USER
        # =========================

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # =========================
        # LOGIN SUCCESS
        # =========================

        if user is not None:

            login(
                request,
                user
            )

            # Protected page redirect
            next_url = (
                request.POST.get('next')
                or request.GET.get('next')
            )

            if next_url:

                return redirect(
                    next_url
                )

            # Normal login -> Home
            return redirect(
                '/home/'
            )

        # =========================
        # LOGIN FAILED
        # =========================

        return render(
            request,
            'cars/login.html',
            {
                'error': 'Username or password is incorrect.'
            }
        )

    # =========================
    # GET -> LOGIN PAGE
    # =========================

    return render(
        request,
        'cars/login.html'
    )


# =============================================
# LOGOUT
# =============================================

def user_logout(request):

    logout(
        request
    )

    # Logout -> Login page
    return redirect(
        '/'
    )


# =============================================
# SELL YOUR CAR
# =============================================

@login_required(
    login_url='/login/'
)
def sell_car(request):

    sell_success = False

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

        # =========================
        # VALIDATE SELL FORM
        # =========================

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
                user=request.user,
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

    # =========================
    # RENDER SELL PAGE
    # =========================

    return render(
        request,
        'cars/sell.html',
        {
            'sell_success': sell_success,
        }
    )


# =============================================
# PROFILE
# =============================================

@login_required(login_url='/login/')
def profile(request):

    return render(
        request,
        'cars/profile.html',
        {
            'profile_user': request.user,
        }
    )