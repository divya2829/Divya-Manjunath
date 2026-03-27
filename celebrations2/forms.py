from django import forms
from .models import Booking
from .models import ThemeBooking
from datetime import date
from .models import ContactMessage
from django.contrib.auth.models import User
from .models import Theme, Venue, Booking, ThemeBooking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'venue', 'payment']
        widgets = {
            'venue': forms.TextInput(attrs={'readonly': 'readonly'}),
            'payment': forms.TextInput(attrs={'readonly': 'readonly'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class ThemeBookingForm(forms.ModelForm):
    class Meta:
        model = ThemeBooking
        fields = ['selected_theme', 'name', 'phone', 'email', 'date', 'start_time', 'end_time']
        widgets = {
            'selected_theme': forms.HiddenInput(),
            'date': forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if not all(x.isalpha() or x.isspace() for x in name):
            raise forms.ValidationError("Name must contain only letters and spaces.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")
        if start and end and start >= end:
            raise forms.ValidationError("End time must be later than start time.")


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not all(x.isalpha() or x.isspace() for x in name):
            raise forms.ValidationError("Name must contain only letters and spaces.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone
    
    # forms.py


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if password and len(password) < 8:
            raise forms.ValidationError("Password must be more than 8 characters.")

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name', 'description', 'cost', 'image']# or list the specific fields

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'location', 'capacity', 'image','description']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

class ThemeBookingForm(forms.ModelForm):
    class Meta:
        model = ThemeBooking
        fields = '__all__'