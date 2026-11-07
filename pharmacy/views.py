
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Pharmacy, Medicine, SearchHistory


# 1. HOME PAGE
def home(request):
    total_pharmacies = Pharmacy.objects.count()
    total_medicines = Medicine.objects.count()
    total_24_open = Pharmacy.objects.filter(is_open_24=True).count()

    return render(request, 'pharmacy/home.html', {
        'total_pharmacies': total_pharmacies,
        'total_medicines': total_medicines,
        'total_24_open': total_24_open
    })


# 2. REGISTER PAGE
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')

        if not username or not password:
            messages.error(request, "Username and password are required!")

        elif password != confirm:
            messages.error(request, "Passwords do not match!")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")

        else:
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            messages.success(request, "Registered Successfully! Now Login.")
            return redirect('/login/')

    return render(request, 'pharmacy/register.html')


# 3. LOGIN PAGE
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/medicines/')

        else:
            messages.error(request, "Wrong Username / Password!")

    return render(request, 'pharmacy/login.html')


# 4. LOGOUT
def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('/')


# 5. MEDICINES SEARCH PAGE
def medicines(request):
    query = request.GET.get('q', '').strip()
    highway = request.GET.get('highway', '').strip()
    category = request.GET.get('category', '').strip()

    results = Medicine.objects.filter(is_available=True)

    if query:
        results = results.filter(name__icontains=query)

        if request.user.is_authenticated:
            SearchHistory.objects.create(
                user=request.user,
                medicine_name=query,
                highway=highway
            )

    if category:
        results = results.filter(category=category)

    if highway:
        results = results.filter(
            pharmacies__highway=highway
        ).distinct()

    return render(request, 'pharmacy/medicines.html', {
        'results': results,
        'query': query,
        'highway': highway,
        'category': category
    })


# 6. PHARMACIES / SHOPS LOCATION PAGE
def pharmacies(request):
    highway = request.GET.get('highway', '')
    medicine_id = request.GET.get('medicine', '')
    query = request.GET.get('q', '')
    open24 = request.GET.get('open24', '')

    medicine = None

    # Case 1: Medicine click chesi vachinappudu
    if medicine_id:
        medicine = get_object_or_404(Medicine, id=medicine_id)
        shops = medicine.pharmacies.all()

    # Case 2: Medicine name tho search chesinappudu
    elif query:
        medicines_found = Medicine.objects.filter(name__icontains=query)
        shops = Pharmacy.objects.filter(medicines__in=medicines_found).distinct()
        # Medicine ki shop link lekapothe, highway shops anni chupinchu
        if not shops.exists():
            shops = Pharmacy.objects.all()

    # Case 3: Direct shops page
    else:
        shops = Pharmacy.objects.all()

    # Highway Filter - NH-65 / NH-16 / NH-44
    if highway:
        shops = shops.filter(highway=highway)

    # 24/7 Open Filter
    if open24 == '1':
        shops = shops.filter(is_open_24=True)

    return render(request, 'pharmacy/pharmacies.html', {
        'shops': shops,
        'medicine': medicine,
        'highway': highway,
        'query': query,
        'open24': open24
    })
