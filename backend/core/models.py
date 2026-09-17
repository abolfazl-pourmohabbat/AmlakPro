from django.db import models
from django.utils.text import slugify

class OfficeProfile(models.Model):
    name = models.CharField(max_length=160, default='دفتر املاک')
    phone = models.CharField(max_length=30, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'اطلاعات دفتر'
        verbose_name_plural = 'اطلاعات دفتر'

class Agent(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='agents/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Property(models.Model):
    SALE = 'sale'; RENT = 'rent'; MORTGAGE = 'mortgage'
    DEAL_TYPES = [(SALE, 'فروش'), (RENT, 'اجاره'), (MORTGAGE, 'رهن')]
    APARTMENT = 'apartment'; HOUSE = 'house'; VILLA = 'villa'; LAND = 'land'; COMMERCIAL = 'commercial'
    TYPES = [(APARTMENT, 'آپارتمان'), (HOUSE, 'خانه'), (VILLA, 'ویلا'), (LAND, 'زمین'), (COMMERCIAL, 'تجاری')]
    AVAILABLE = 'available'; NEGOTIATING = 'negotiating'; SOLD = 'sold'; RENTED = 'rented'
    STATUS = [(AVAILABLE, 'موجود'), (NEGOTIATING, 'در مذاکره'), (SOLD, 'فروخته شد'), (RENTED, 'اجاره رفت')]
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    deal_type = models.CharField(max_length=20, choices=DEAL_TYPES)
    property_type = models.CharField(max_length=20, choices=TYPES)
    city = models.CharField(max_length=80)
    district = models.CharField(max_length=120)
    address = models.CharField(max_length=300, blank=True)
    area = models.PositiveIntegerField()
    bedrooms = models.PositiveSmallIntegerField(default=0)
    floor = models.CharField(max_length=20, blank=True)
    built_year = models.PositiveSmallIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    deposit = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    rent = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    description = models.TextField(blank=True)
    parking = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    storage = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS, default=AVAILABLE)
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'property'
            slug = base
            n = 2
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self): return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='properties/gallery/')
    caption = models.CharField(max_length=180, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self): return f'{self.property.title} - {self.id}'

class Lead(models.Model):
    NEW = 'new'; CONTACTED = 'contacted'; VISIT = 'visit'; CLOSED = 'closed'; CANCELLED = 'cancelled'
    STATUSES = [(NEW, 'جدید'), (CONTACTED, 'تماس گرفته شد'), (VISIT, 'بازدید'), (CLOSED, 'معامله شد'), (CANCELLED, 'لغو شد')]
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    message = models.TextField(blank=True)
    preferred_time = models.CharField(max_length=100, blank=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    status = models.CharField(max_length=20, choices=STATUSES, default=NEW)
    source = models.CharField(max_length=40, default='website', blank=True)
    assigned_agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    notes = models.TextField(blank=True)
    next_follow_up = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.name} - {self.phone}'

class LeadActivity(models.Model):
    CALL = 'call'; NOTE = 'note'; VISIT = 'visit'; STATUS = 'status'
    TYPES = [(CALL, 'تماس'), (NOTE, 'یادداشت'), (VISIT, 'بازدید'), (STATUS, 'تغییر وضعیت')]
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=TYPES, default=NOTE)
    text = models.TextField()
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.lead.name} - {self.activity_type}'

class Favorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'property'], name='unique_user_property_favorite')]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.property.title}'
