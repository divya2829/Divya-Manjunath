from django.db import models
from django.utils.text import slugify

class Venue(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    image = models.ImageField(upload_to='venues/', blank=True, null=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Automatically generate slug from name if not set
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    date = models.DateField()
    venue = models.CharField(max_length=200)
    payment = models.CharField(max_length=100, default="Only cash is accepted")

    def __str__(self):
        return f"{self.name} - {self.venue} on {self.date}"
    
    from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='themes_images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    from django.db import models

THEME_CHOICES = [
    # Birthday Themes
    ('birthday_candy', 'Birthday Candy Theme'),
    ('birthday_green', 'Birthday Green Theme'),
    ('birthday_skyblue', 'Birthday Sky Blue Theme'),
    ('birthday_paradise', 'Birthday Paradise Theme'),
    ('birthday_peacock', 'Birthday Peacock Theme'),

    # Halsi Themes (Haldi ceremony)
    ('halsi_traditional', 'Halsi Traditional Theme'),
    ('halsi_floral', 'Halsi Floral Theme'),
    ('halsi_bright', 'Halsi Bright Theme'),

    # Bride Themes
    ('bride_red', 'Bride Red Theme'),
    ('bride_pink', 'Bride Pink Theme'),
    ('bride_glam', 'Bride Glamorous Theme'),

    # Baby Shower Themes
    ('baby_blue', 'Baby Blue Theme'),
    ('baby_pink', 'Baby Pink Theme'),
    ('baby_yellow', 'Baby Yellow Theme'),

    # Nikka Themes (Nikah / Wedding)
    ('nikka_red', 'Nikka Red Theme'),
    ('nikka_indoor', 'Nikka Indoor Theme'),
    ('nikka_outdoor', 'Nikka Outdoor Theme'),
    ('nikka_yellow', 'Nikka Yellow Theme'),

    # General themes
    ('candy', 'Candy Theme'),
    ('green', 'Green Theme'),
    ('skyblue', 'Sky Blue Theme'),
    ('paradise', 'Paradise Theme'),
    ('peacock', 'Peacock Theme'),
]

class ThemeBooking(models.Model):
    selected_theme = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


    def __str__(self):
        return f"{self.name} - {self.selected_theme}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Theme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='themes/')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Venue(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)            # add this field
    description = models.TextField(blank=True)       # add this field
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='venues/')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while Venue.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
