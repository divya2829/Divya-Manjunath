from django.urls import path
from . import views
from .views import booking_view
from .views import contact_view  
from .views import user_login_view, admin_login_view
from .views import ThemeDeleteView




urlpatterns = [
    path('', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('forgot/', views.forgot_password_view, name='forgot_password'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('Venue/', views.venue, name='Venue'),
    path('themes/', views.themes, name='themes'),
    path('contact/', contact_view, name='contact'),  
    path('venues/', views.venue_list, name='venue_list'),
    path('venues/<slug:slug>/', views.venue_detail, name='venue_detail'),
    path('petals/', views.petals, name='petals'),
    path('mannat/', views.mannat, name='mannat'),
    path('blue_pearl/', views.blue_pearl, name='blue_pearl'),
    path('chamara/', views.chamara, name='chamara'),
    path('palace/', views.palace, name='palace'),
    path('peacock/', views.peacock, name='peacock'),
    path('lalitha/', views.lalitha, name='lalitha'),
    path('leela/', views.leela, name='leela'),
    path('booking/', booking_view, name='booking'),
    path('themes/', views.themes, name='themes'),
    path('themes/<slug:slug>/', views.theme_detail, name='theme_detail'),
    path('birthday/', views.birthday, name='birthday'),
    path('haldi/', views.haldi, name='haldi'),
    path('bride/', views.bride, name='bride'),
    path('baby/', views.baby, name='baby'),
    path('nikah/', views.nikah, name='nikah'),
    path('yellow/', views.yellow, name='yellow'),
    path('cartoon/', views.cartoon, name='cartoon'),
    path('candy/', views.candy, name='candy'),
    path('green/', views.green, name='green'),
    path('skyblue/', views.skyblue, name='skyblue'),
    path('black/', views.black, name='black'),
    path('flower/', views.flower, name='flower'),
    path('greenhaldi/', views.greenhaldi, name='greenhaldi'),
    path('paradise/', views.paradise, name='paradise'),
    path('pink/', views.pink, name='pink'),
    path('yellowhaldi/', views.yellowhaldi, name='yellowhaldi'),
    path('brown/', views.brown_theme, name='brown_theme'),
    path('gold/', views.bridegold_theme, name='bridegold_theme'),
    path('pink/', views.bridepink_theme, name='bridepink_theme'),
    path('white/', views.bridewhite_theme, name='bridewhite_theme'),
    path('krishna/', views.krishna_theme, name='krishna_theme'),
    path('green/', views.shower_green, name='shower_green'),
    path('peacock/', views.shower_peacock, name='shower_peacock'),
    path('flower/', views.shower_flower, name='shower_flower'),
    path('white/', views.shower_white, name='shower_white'),
    path('yellow/', views.shower_yellow, name='shower_yellow'),
    path('red/', views.nikkared, name='nikkared'),
    path('indoor/', views.nikkaindoor, name='nikkaindoor'),
    path('outdoor/', views.nikkaoutdoor, name='nikkaoutdoor'),
    path('theme-booking/', views.theme_booking, name='theme_booking'),
    path('confirm-booking/', views.confirm_booking, name='confirm_booking'),  # <-- This must be present
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('dashboard/themes/', views.theme_list, name='theme_list'),
    path('dashboard/themes/create/', views.theme_create, name='theme_create'),
    path('dashboard/themes/edit/<int:pk>/', views.theme_edit, name='theme_edit'),
    path('dashboard/themes/delete/<int:pk>/', ThemeDeleteView.as_view(), name='theme_delete'),

# Venue URLs
    path('dashboard/venues/', views.dashboard_venue_list, name='venue_list'),
    path('dashboard/venues/create/', views.venue_create, name='venue_create'),
    path('dashboard/venues/edit/<int:pk>/', views.venue_edit, name='venue_edit'),
    path('dashboard/venues/delete/<int:pk>/', views.venue_delete, name='venue_delete'),
    # Booking URLs
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/edit/<int:id>/', views.edit_booking, name='edit_booking'),
    path('bookings/delete/<int:id>/', views.delete_booking, name='delete_booking'),
    path('theme-bookings/', views.theme_booking_list, name='theme_booking_list'),
    path('theme-bookings/edit/<int:pk>/', views.edit_theme_booking, name='edit_theme_booking'),
    path('theme-bookings/delete/<int:pk>/', views.delete_theme_booking, name='delete_theme_booking'),
    path('users/', views.user_list, name='user_list'),
    path('login/user/', user_login_view, name='user_login'),
    path('login/admin/', admin_login_view, name='admin_login'),












]



