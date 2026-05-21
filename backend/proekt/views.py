from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, BookingForm, ReviewForm
from .models import UserProfile, Hall, Booking, Review

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone']
            )
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('index')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('login')

@login_required
def index_view(request):
    halls = Hall.objects.all()
    
    if not halls.exists():
        halls_data = [
            ('Аудитория', 50, 'Просторная аудитория с проектором', 1500),
            ('Коворкинг', 30, 'Современное пространство для работы', 2000),
            ('Кинозал', 100, 'Профессиональный кинозал с акустикой', 5000),
        ]
        for name, capacity, desc, price in halls_data:
            Hall.objects.get_or_create(name=name, defaults={
                'capacity': capacity, 
                'description': desc, 
                'price_per_hour': price
            })
        halls = Hall.objects.all()
    
    return render(request, 'index.html', {'halls': halls})

@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(
            user=request.user,
            full_name=request.user.get_full_name() or request.user.username,
            phone='8(000)000-00-00'  
        )
    
    user_bookings = Booking.objects.filter(user=request.user)
    total_bookings = user_bookings.count()
    
    # Статистика по статусам
    new_bookings = user_bookings.filter(status='Новая').count()
    scheduled_bookings = user_bookings.filter(status='Мероприятие назначено').count()
    completed_bookings = user_bookings.filter(status='Мероприятие завершено').count()
    
    # Последние 5 бронирований
    recent_bookings = user_bookings[:5]
    
    context = {
        'user_profile': user_profile,
        'total_bookings': total_bookings,
        'new_bookings': new_bookings,
        'scheduled_bookings': scheduled_bookings,
        'completed_bookings': completed_bookings,
        'recent_bookings': recent_bookings,
    }
    
    return render(request, 'profile.html', context)

@login_required
def bookings_view(request):
    user_bookings = Booking.objects.filter(user=request.user)
    
    if request.method == 'POST' and 'review_booking_id' in request.POST:
        booking_id = request.POST.get('review_booking_id')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        if booking.status == 'Мероприятие завершено':
            if not hasattr(booking, 'review'):
                review_form = ReviewForm(request.POST)
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.booking = booking
                    review.user = request.user
                    review.save()
                    messages.success(request, 'Спасибо за ваш отзыв!')
                else:
                    messages.error(request, 'Ошибка при сохранении отзыва')
            else:
                messages.warning(request, 'Вы уже оставили отзыв на это мероприятие')
        else:
            messages.error(request, 'Отзыв можно оставить только после завершения мероприятия')
        return redirect('bookings')
    
    paginator = Paginator(user_bookings, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    review_form = ReviewForm()
    
    return render(request, 'bookings.html', {
        'bookings': page_obj,
        'review_form': review_form,
    })

@login_required
def create_booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Заявка на бронирование успешно отправлена на рассмотрение!')
            return redirect('bookings')
    else:
        form = BookingForm()
    
    return render(request, 'create_booking.html', {'form': form})