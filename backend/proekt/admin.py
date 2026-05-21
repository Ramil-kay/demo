from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Hall, Booking, Review

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'get_full_name', 'get_phone', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'profile__full_name', 'profile__phone']
    
    def get_full_name(self, obj):
        return obj.profile.full_name if hasattr(obj, 'profile') else ''
    get_full_name.short_description = 'ФИО'
    
    def get_phone(self, obj):
        return obj.profile.phone if hasattr(obj, 'profile') else ''
    get_phone.short_description = 'Телефон'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'price_per_hour']
    list_filter = ['name']
    search_fields = ['name', 'description']
    list_editable = ['capacity', 'price_per_hour']
    list_per_page = 10  # Пагинация

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'hall', 'event_date', 'start_time', 'status', 'created_at']
    list_filter = ['status', 'hall', 'event_date', 'user']
    search_fields = ['user__username', 'user__email', 'hall__name']
    list_editable = ['status']
    list_per_page = 15  # Пагинация
    date_hierarchy = 'event_date'  # Навигация по датам
    
    actions = ['mark_as_scheduled', 'mark_as_completed']
    
    def mark_as_scheduled(self, request, queryset):
        queryset.update(status='Мероприятие назначено')
    mark_as_scheduled.short_description = 'Изменить статус на "Мероприятие назначено"'
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='Мероприятие завершено')
    mark_as_completed.short_description = 'Изменить статус на "Мероприятие завершено"'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'comment']
    list_per_page = 20