from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Venue
from django.contrib import admin
from .models import Booking
from .forms import BookingForm
from django.urls import reverse
from .models import Theme
from .models import ThemeBooking
from .forms import ThemeBookingForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from .forms import ContactMessageForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ThemeForm, VenueForm, BookingForm, ThemeBookingForm  # We'll create forms for these
from django.views.generic import DeleteView
from django.urls import reverse_lazy



def login_view(request):
    return render(request, 'login_main.html')

def user_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('index')  # or user dashboard
        else:
            messages.error(request, 'Invalid user credentials.')
    return render(request, 'login_user.html')


def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')  # or wherever admin should land
        else:
            messages.error(request, 'Invalid admin credentials.')
    return render(request, 'login_admin.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Simple validations
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')  # Replace with your login URL name

    return render(request, 'registration.html')

def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_staff)(view_func))
    return decorated_view_func

@admin_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_bookings = Booking.objects.count()
    total_theme_bookings = ThemeBooking.objects.count()
    total_themes = Theme.objects.count()
    total_venues = Venue.objects.count()

    context = {
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_theme_bookings': total_theme_bookings,
        'total_themes': total_themes,
        'total_venues': total_venues,
    }
    return render(request, 'admin_dashboard.html', context)

@admin_required
def theme_list(request):
    themes = Theme.objects.all()
    return render(request, 'dashboard/theme_list.html', {'themes': themes})

@admin_required
def theme_create(request):
    if request.method == "POST":
        form = ThemeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Theme created successfully.")
            return redirect('theme_list')
    else:
        form = ThemeForm()
    return render(request, 'dashboard/theme_form.html', {'form': form})

@admin_required
def theme_edit(request, pk):
    theme = get_object_or_404(Theme, pk=pk)
    if request.method == "POST":
        form = ThemeForm(request.POST, request.FILES, instance=theme)
        if form.is_valid():
            form.save()
            messages.success(request, "Theme updated successfully.")
            return redirect('theme_list')
    else:
        form = ThemeForm(instance=theme)
    return render(request, 'dashboard/theme_form.html', {'form': form})

@admin_required
def theme_delete(request, pk):
    theme = get_object_or_404(Theme, pk=pk)
    if request.method == "POST":
        theme.delete()
        messages.success(request, "Theme deleted successfully.")
        return redirect('theme_list')
    return render(request, 'theme_confirm_delete.html', {'theme': theme})

class ThemeDeleteView(DeleteView):
    model = Theme
    template_name = 'theme_confirm_delete.html'  # or your custom template path
    success_url = reverse_lazy('theme_list')

@admin_required
def dashboard_venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'dashboard/venue_list.html', {'venues': venues})

@admin_required
def venue_create(request):
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('venue_list')
    else:
        form = VenueForm()
    return render(request, 'dashboard/venue_form.html', {'form': form, 'title': 'Add New Venue'})

@admin_required
def venue_edit(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            messages.success(request, "Venue updated successfully.")
            return redirect('venue_list')
    else:
        form = VenueForm(instance=venue)
    return render(request, 'dashboard/venue_form.html', {'form': form})

@admin_required
def venue_delete(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    if request.method == "POST":
        venue.delete()
        messages.success(request, "Venue deleted successfully.")
        return redirect('venue_list')
    return render(request, 'dashboard/venue_confirm_delete.html', {'venue': venue})




@admin_required
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking_list.html', {'bookings': bookings})

@admin_required
def edit_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    if request.method == 'POST':
        booking.name = request.POST['name']
        booking.email = request.POST['email']
        booking.phone = request.POST['phone']
        booking.date = request.POST['date']
        booking.venue = request.POST['venue']
        booking.payment = request.POST['payment']
        booking.save()
        return redirect('booking_list')
    return render(request, 'edit_booking.html', {'booking': booking})

@admin_required
def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    return redirect('booking_list')

# Theme Bookings

@admin_required
def theme_booking_list(request):
    bookings = ThemeBooking.objects.all()
    return render(request, 'theme_booking_list.html', {'bookings': bookings})

@admin_required

def edit_theme_booking(request, pk):
    booking = get_object_or_404(ThemeBooking, pk=pk)
    if request.method == 'POST':
        form = ThemeBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('theme_booking_list')
    else:
        form = ThemeBookingForm(instance=booking)
    return render(request, 'edit_theme_booking.html', {'form': form})


@admin_required
def delete_theme_booking(request, pk):
    booking = get_object_or_404(ThemeBooking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('theme_booking_list')
    return render(request, 'delete_theme_booking.html', {'booking': booking})


@admin_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')

    return render(request, 'registration.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            user.set_password('newpassword123')  # You can generate a random one here
            user.save()
            messages.success(request, "Password reset. Your new password is 'newpassword123'")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
    return render(request, 'forgot.html')

def booking_view(request):
    initial_data = {}
    venue = request.GET.get('venue')
    if venue:
        initial_data['venue'] = venue
    initial_data['payment'] = "Only cash is accepted"

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # Generate PDF confirmation
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            p.setFont("Helvetica-Bold", 20)
            p.drawString(50, height - 50, "Booking Confirmation")

            p.setFont("Helvetica", 12)
            p.drawString(50, height - 100, f"Name: {booking.name}")
            p.drawString(50, height - 120, f"Email: {booking.email}")
            p.drawString(50, height - 140, f"Phone: {booking.phone}")
            p.drawString(50, height - 160, f"Venue: {booking.venue}")
            p.drawString(50, height - 180, f"Date: {booking.date}")
            p.drawString(50, height - 200, f"Payment: {booking.payment}")

            p.drawString(50, height - 240, "Thank you for booking with us!")
            p.showPage()
            p.save()

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Booking_{booking.name}.pdf"'
            return response

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm(initial=initial_data)

    return render(request, 'booking.html', {'form': form})

def theme_booking(request):
    selected_theme = request.GET.get('theme', '')

    if request.method == 'POST':
        form = ThemeBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking confirmed! You will receive a PDF confirmation soon.")
            # Redirect back to booking page without POST data, keep theme param
            return redirect(f"{reverse('theme_booking')}?theme={selected_theme}")
    else:
        form = ThemeBookingForm(initial={'theme': selected_theme})

    return render(request, 'themebooking.html', {'form': form, 'selected_theme': selected_theme})

def confirm_booking(request):
    if request.method == 'POST':
        selected_theme = request.POST.get('selectedTheme')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        booking = ThemeBooking(
            selected_theme=selected_theme,  # ✅ Use correct field name here
            name=name,
            phone=phone,
            email=email,
            date=date,
            start_time=start_time,
            end_time=end_time
        )
        booking.save()

        # Create PDF in memory
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # PDF content
        p.setFont("Helvetica-Bold", 20)
        p.drawString(50, height - 50, "Booking Confirmation")

        p.setFont("Helvetica", 12)
        p.drawString(50, height - 100, f"Name: {name}")
        p.drawString(50, height - 120, f"Email: {email}")
        p.drawString(50, height - 140, f"Phone: {phone}")
        p.drawString(50, height - 160, f"Theme: {selected_theme}")
        p.drawString(50, height - 180, f"Date: {date}")
        p.drawString(50, height - 200, f"Time: {start_time} to {end_time}")

        p.drawString(50, height - 240, "Thank you for booking with us!")
        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Booking_{name}.pdf"'

        return response

    return redirect('theme_booking')

def contact_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us! We will get back to you soon.")
            return redirect('contact')  # Assuming URL name is 'contact'
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactMessageForm()

    return render(request, 'contact.html', {'form': form})


# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'aboutus.html')

def gallery(request):
    return render(request, 'gallery.html')

def venue(request):
    return render(request, 'venue.html') 

def themes(request):
    return render(request, 'themes.html')

def contact(request):
    return render(request, 'contact.html')

# venues

def venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'venue.html', {'venues': venues})

def venue_detail(request, slug):
    venue = get_object_or_404(Venue, slug=slug)
    return render(request, 'venue_detail.html', {'venue': venue})

def petals(request):
    return render(request, 'petals.html')

def mannat(request):
    return render(request, 'mannat.html')

def blue_pearl(request):
    return render(request, 'blue_pearl.html')

def chamara(request):
    return render(request, 'chamara.html')

def palace(request):
    return render(request, 'palace.html')

def peacock(request):
    return render(request, 'peacock.html')

def lalitha(request):
    return render(request, 'lalitha.html')

def leela(request):
    return render(request, 'leela.html')

# Themes

def themes(request):
    all_themes = Theme.objects.all()
    return render(request, 'themes.html', {'themes': all_themes})

def theme_detail(request, slug):
    theme = get_object_or_404(Theme, slug=slug)
    return render(request, 'theme_detail.html', {'theme': theme})

def birthday(request):
    return render(request, 'birthday.html')

def haldi(request):
    return render(request, 'haldi.html')

def bride(request):
    return render(request, 'bride.html')

def baby(request):
    return render(request, 'baby.html')

def nikah(request):
    return render(request, 'nikah.html')

def yellow(request):
    return render(request, 'yellow.html')

def cartoon(request):
    return render(request, 'cartoon.html')

def candy(request):
    return render(request, 'candy.html')

def green(request):
    return render(request, 'green.html')

def skyblue(request):
    return render(request, 'skyblue.html')

def black(request):
    return render(request, 'black.html')

def flower(request):
    return render(request, 'flower.html')

def greenhaldi(request):
    return render(request, 'greenhaldi.html')

def paradise(request):
    return render(request, 'paradise.html')

def pink(request):
    return render(request, 'pink.html')

def yellowhaldi(request):
    return render(request, 'yellowhaldi.html')

def brown_theme(request):
    return render(request, 'brown.html')

def bridegold_theme(request):
    return render(request, 'bridegold.html')

def bridepink_theme(request):
    return render(request, 'bridepink.html')

def bridewhite_theme(request):
    return render(request, 'bridewhite.html')

def krishna_theme(request):
    return render(request, 'krishna.html')

def shower_green(request):
    return render(request, 'shower_green.html')

def shower_peacock(request):
    return render(request, 'shower_peacock.html')

def shower_flower(request):
    return render(request, 'shower_flower.html')

def shower_white(request):
    return render(request, 'shower_white.html')

def shower_yellow(request):
    return render(request, 'shower_yellow.html')

def nikkared(request):
    return render(request, 'nikkared.html')

def nikkaindoor(request):
    return render(request, 'nikkaindoor.html')

def nikkaoutdoor(request):
    return render(request, 'nikkaoutdoor.html')

