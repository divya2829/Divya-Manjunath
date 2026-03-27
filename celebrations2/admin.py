from django.contrib import admin
from .models import Booking
from .models import Venue
from .models import ThemeBooking
from .models import ContactMessage
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

# Optional: Customize the admin display
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

# Unregister and re-register if you want to customize
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date', 'venue', 'payment')
    list_filter = ('date', 'venue')
    search_fields = ('name', 'email', 'phone', 'venue')

@admin.register(ThemeBooking)
class ThemeBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'selected_theme', 'date', 'start_time', 'end_time', 'email', 'phone', 'image_preview')
    list_filter = ('selected_theme', 'date')
    search_fields = ('name', 'email', 'phone', 'selected_theme')
    ordering = ('-date', 'start_time')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    readonly_fields = ('submitted_at',)
# Register your models here.

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'short_description', 'venue_image')

    def venue_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover;" />', obj.image.url)
        return "-"
    venue_image.short_description = 'Image'

    def short_description(self, obj):
        if obj.description:
            return (obj.description[:75] + '...') if len(obj.description) > 75 else obj.description
        return "-"
    short_description.short_description = 'Description'

