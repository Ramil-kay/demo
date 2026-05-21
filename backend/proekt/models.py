from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$',
                message='Телефон должен быть в формате: 8(XXX)XXX-XX-XX'
            )
        ]
    )
    full_name = models.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[А-Яа-яЁё\s]+$',
                message='ФИО должно содержать только буквы кириллицы и пробелы'
            )
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Hall(models.Model):
    HALL_CHOICES = [
        ('Аудитория', 'Аудитория'),
        ('Коворкинг', 'Коворкинг'),
        ('Кинозал', 'Кинозал'),
    ]
    
    name = models.CharField(max_length=50, choices=HALL_CHOICES, unique=True)
    capacity = models.IntegerField(verbose_name='Вместимость')
    description = models.TextField(blank=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.name} (вместимость: {self.capacity})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Новая', 'Новая'),
        ('Мероприятие назначено', 'Мероприятие назначено'),
        ('Мероприятие завершено', 'Мероприятие завершено'),
    ]
    
    PAYMENT_CHOICES = [
        ('наличными', 'Наличными'),
        ('перевод по номеру телефона', 'Перевод по номеру телефона'),
        ('банковская карта', 'Банковская карта'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='bookings')
    event_date = models.DateField(verbose_name='Дата проведения')
    start_time = models.TimeField(verbose_name='Время начала')
    duration_hours = models.IntegerField(default=2, verbose_name='Длительность (часы)')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Новая')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Бронирование #{self.id} - {self.user.username} - {self.hall.name}"

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Отзыв от {self.user.username} к бронированию #{self.booking.id}"