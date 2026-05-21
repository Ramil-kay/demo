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
    search_fields = ['name']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'hall', 'event_date', 'start_time', 'status', 'created_at']
    list_filter = ['status', 'hall', 'event_date']
    search_fields = ['user__username', 'user__email']
    list_editable = ['status']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']