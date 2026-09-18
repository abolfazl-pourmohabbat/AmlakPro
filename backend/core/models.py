from django.db import models
from django.utils.text import slugify

class OfficeProfile(models.Model):
    translations=models.JSONField(default=dict, blank=True)
    name=models.CharField(max_length=160,default='دفتر املاک'); phone=models.CharField(max_length=30,blank=True); mobile=models.CharField(max_length=30,blank=True); address=models.CharField(max_length=300,blank=True); city=models.CharField(max_length=80,blank=True); description=models.TextField(blank=True); updated_at=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
        if self.translations is None: self.translations={}
        super().save(*args,**kwargs)
    def __str__(self): return self.name
    class Meta: verbose_name='اطلاعات دفتر'; verbose_name_plural='اطلاعات دفتر'
class Agent(models.Model):
    translations=models.JSONField(default=dict, blank=True)
    name=models.CharField(max_length=120); role=models.CharField(max_length=120,blank=True); phone=models.CharField(max_length=30); bio=models.TextField(blank=True); image=models.ImageField(upload_to='agents/',blank=True,null=True); is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if self.translations is None: self.translations={}
        super().save(*args,**kwargs)
    def __str__(self): return self.name
class Property(models.Model):
    translations=models.JSONField(default=dict, blank=True)
    SALE='sale'; RENT='rent'; MORTGAGE='mortgage'; DEAL_TYPES=[(SALE,'فروش'),(RENT,'اجاره'),(MORTGAGE,'رهن')]; APARTMENT='apartment'; HOUSE='house'; VILLA='villa'; LAND='land'; COMMERCIAL='commercial'; TYPES=[(APARTMENT,'آپارتمان'),(HOUSE,'خانه'),(VILLA,'ویلا'),(LAND,'زمین'),(COMMERCIAL,'تجاری')]; AVAILABLE='available'; NEGOTIATING='negotiating'; SOLD='sold'; RENTED='rented'; STATUS=[(AVAILABLE,'موجود'),(NEGOTIATING,'در مذاکره'),(SOLD,'فروخته شد'),(RENTED,'اجاره رفت')]
    title=models.CharField(max_length=220); slug=models.SlugField(unique=True,blank=True); deal_type=models.CharField(max_length=20,choices=DEAL_TYPES); property_type=models.CharField(max_length=20,choices=TYPES); city=models.CharField(max_length=80); district=models.CharField(max_length=120); address=models.CharField(max_length=300,blank=True); area=models.PositiveIntegerField(); bedrooms=models.PositiveSmallIntegerField(default=0); floor=models.CharField(max_length=20,blank=True); built_year=models.PositiveSmallIntegerField(blank=True,null=True); price=models.DecimalField(max_digits=18,decimal_places=0,default=0); deposit=models.DecimalField(max_digits=18,decimal_places=0,default=0); rent=models.DecimalField(max_digits=18,decimal_places=0,default=0); description=models.TextField(blank=True); parking=models.BooleanField(default=False); elevator=models.BooleanField(default=False); storage=models.BooleanField(default=False); balcony=models.BooleanField(default=False); featured=models.BooleanField(default=False); status=models.CharField(max_length=20,choices=STATUS,default=AVAILABLE); image=models.ImageField(upload_to='properties/',blank=True,null=True); agent=models.ForeignKey(Agent,on_delete=models.SET_NULL,null=True,blank=True,related_name='properties'); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
        if self.translations is None: self.translations={}
        if not self.slug:
            base=slugify(self.title) or 'property'; slug=base; n=2
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists(): slug=f'{base}-{n}'; n+=1
            self.slug=slug
        super().save(*args,**kwargs)
    def __str__(self): return self.title
class PropertyImage(models.Model):
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name='gallery'); image=models.ImageField(upload_to='properties/gallery/'); caption=models.CharField(max_length=180,blank=True); sort_order=models.PositiveSmallIntegerField(default=0); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['sort_order','id']
    def __str__(self): return f'{self.property.title} - {self.id}'
class Lead(models.Model):
    NEW='new'; CONTACTED='contacted'; VISIT='visit'; CLOSED='closed'; CANCELLED='cancelled'; STATUSES=[(NEW,'جدید'),(CONTACTED,'تماس گرفته شد'),(VISIT,'بازدید'),(CLOSED,'معامله شد'),(CANCELLED,'لغو شد')]
    name=models.CharField(max_length=120); phone=models.CharField(max_length=30); message=models.TextField(blank=True); preferred_time=models.CharField(max_length=100,blank=True); property=models.ForeignKey(Property,on_delete=models.SET_NULL,null=True,blank=True,related_name='leads'); status=models.CharField(max_length=20,choices=STATUSES,default=NEW); source=models.CharField(max_length=40,default='website',blank=True); assigned_agent=models.ForeignKey(Agent,on_delete=models.SET_NULL,null=True,blank=True,related_name='leads'); notes=models.TextField(blank=True); next_follow_up=models.DateTimeField(null=True,blank=True); updated_at=models.DateTimeField(auto_now=True); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.name} - {self.phone}'
class LeadActivity(models.Model):
    CALL='call'; NOTE='note'; VISIT='visit'; STATUS='status'; TYPES=[(CALL,'تماس'),(NOTE,'یادداشت'),(VISIT,'بازدید'),(STATUS,'تغییر وضعیت')]
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='activities'); activity_type=models.CharField(max_length=20,choices=TYPES,default=NOTE); text=models.TextField(); created_by=models.ForeignKey('auth.User',on_delete=models.SET_NULL,null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'{self.lead.name} - {self.activity_type}'
class SiteSettings(models.Model):
    site_name=models.CharField(max_length=120,default='املاک پرو'); site_tagline=models.CharField(max_length=220,default='خانه‌ای که دنبالش هستید، پیدا می‌کنیم.'); logo=models.ImageField(upload_to='site/',blank=True,null=True); hero_image=models.ImageField(upload_to='site/',blank=True,null=True)
    primary_color=models.CharField(max_length=7,default='#b8945c'); secondary_color=models.CharField(max_length=7,default='#11110f'); background_color=models.CharField(max_length=7,default='#f5f3ee'); text_color=models.CharField(max_length=7,default='#171714'); accent_color=models.CharField(max_length=7,default='#c6a66e'); line_color=models.CharField(max_length=7,default='#dedbd3')
    nav_home=models.CharField(max_length=60,default='خانه'); nav_properties=models.CharField(max_length=60,default='املاک'); nav_agents=models.CharField(max_length=60,default='مشاوران'); nav_about=models.CharField(max_length=60,default='درباره ما'); nav_contact=models.CharField(max_length=60,default='تماس با ما'); nav_favorites=models.CharField(max_length=60,default='علاقه‌مندی‌ها')
    hero_eyebrow=models.CharField(max_length=160,default='دفتر تخصصی خرید، فروش و اجاره'); hero_title=models.CharField(max_length=220,default='ملک مناسب شما،'); hero_title_emphasis=models.CharField(max_length=120,default='همین‌جاست.'); hero_description=models.TextField(default='با جست‌وجوی دقیق و مشاوره حرفه‌ای، انتخاب بعدی‌تان را مطمئن‌تر کنید.'); hero_search_label=models.CharField(max_length=80,default='جست‌وجو'); hero_search_placeholder=models.CharField(max_length=180,default='مثلاً سعادت‌آباد، آپارتمان ۱۲۰ متری'); hero_deal_label=models.CharField(max_length=80,default='نوع معامله'); hero_search_button=models.CharField(max_length=100,default='جست‌وجوی ملک')
    featured_eyebrow=models.CharField(max_length=100,default='انتخاب‌های ویژه'); featured_title=models.CharField(max_length=180,default='ملک‌هایی که ارزش دیدن دارند'); featured_link=models.CharField(max_length=100,default='مشاهده همه ←'); empty_properties_text=models.CharField(max_length=180,default='هنوز ملک ویژه‌ای ثبت نشده؛ از پنل مدیریت اضافه کنید.')
    trust_1_title=models.CharField(max_length=100,default='مشاوره شفاف'); trust_1_text=models.CharField(max_length=220,default='اطلاعات روشن و قابل بررسی برای تصمیمی بهتر.'); trust_2_title=models.CharField(max_length=100,default='انتخاب دقیق'); trust_2_text=models.CharField(max_length=220,default='فیلترهای کاربردی برای رسیدن سریع‌تر به گزینه مناسب.'); trust_3_title=models.CharField(max_length=100,default='همراه تا معامله'); trust_3_text=models.CharField(max_length=220,default='از اولین تماس تا بازدید و نهایی‌شدن معامله.')
    about_eyebrow=models.CharField(max_length=100,default='شناخت بیشتر'); about_title=models.CharField(max_length=180,default='درباره املاک پرو'); about_intro=models.TextField(default='یک دفتر املاک مدرن برای پیدا کردن، مقایسه و انتخاب مطمئن‌تر ملک.'); about_card_1_title=models.CharField(max_length=120,default='انتخاب ملک، ساده و شفاف'); about_card_1_text=models.TextField(default='در املاک پرو تلاش می‌کنیم اطلاعات ملک‌ها را روشن و کاربردی ارائه کنیم تا مسیر جست‌وجو تا معامله برای شما ساده‌تر باشد.'); about_card_2_title=models.CharField(max_length=120,default='مشاوره تخصصی'); about_card_2_text=models.TextField(default='برای خرید، فروش، رهن و اجاره می‌توانید با مشاوران مجموعه در ارتباط باشید و قبل از تصمیم نهایی اطلاعات لازم را دریافت کنید.'); about_card_3_title=models.CharField(max_length=120,default='همراه تا معامله'); about_card_3_text=models.TextField(default='هدف ما فقط نمایش یک ملک نیست؛ می‌خواهیم از اولین جست‌وجو تا بازدید و نهایی‌شدن معامله، تجربه‌ای منظم و قابل اعتماد داشته باشید.')
    properties_eyebrow=models.CharField(max_length=100,default='املاک'); properties_title=models.CharField(max_length=180,default='گزینه مناسب بعدی شما'); properties_intro=models.TextField(default='جست‌وجو و فیلتر بین املاک موجود دفتر.'); properties_search_placeholder=models.CharField(max_length=180,default='شهر، محله یا نام ملک'); properties_deal_label=models.CharField(max_length=80,default='نوع معامله'); properties_type_label=models.CharField(max_length=80,default='نوع ملک'); properties_ordering_label=models.CharField(max_length=80,default='مرتب‌سازی'); properties_apply_button=models.CharField(max_length=80,default='اعمال فیلتر'); properties_clear_button=models.CharField(max_length=80,default='پاک کردن'); properties_prev_button=models.CharField(max_length=60,default='قبلی'); properties_next_button=models.CharField(max_length=60,default='بعدی'); properties_loading_text=models.CharField(max_length=160,default='در حال دریافت املاک...'); properties_error_text=models.CharField(max_length=180,default='دریافت فهرست املاک انجام نشد.'); properties_empty_text=models.CharField(max_length=180,default='ملکی مطابق جست‌وجوی شما پیدا نشد.'); properties_count_label=models.CharField(max_length=60,default='ملک');
    agents_eyebrow=models.CharField(max_length=100,default='تیم ما'); agents_title=models.CharField(max_length=180,default='مشاورانی که کنار شما هستند'); agents_intro=models.TextField(default='تخصص محلی، پاسخ‌گویی و همراهی تا پایان معامله.'); agents_empty_text=models.CharField(max_length=180,default='هنوز مشاوری ثبت نشده است.'); agents_phone_label=models.CharField(max_length=80,default='تماس با مشاور');
    about_button=models.CharField(max_length=100,default='مشاهده املاک');
    contact_eyebrow=models.CharField(max_length=100,default='در ارتباط باشیم'); contact_title=models.CharField(max_length=120,default='تماس با ما'); contact_intro=models.TextField(default='برای پرسش درباره ملک‌ها، هماهنگی بازدید یا دریافت مشاوره با دفتر املاک پرو در ارتباط باشید.'); contact_office_name_label=models.CharField(max_length=80,default='نام دفتر'); contact_city_label=models.CharField(max_length=80,default='شهر'); contact_description_label=models.CharField(max_length=80,default='معرفی دفتر'); contact_phone_label=models.CharField(max_length=80,default='تلفن دفتر'); contact_mobile_label=models.CharField(max_length=80,default='موبایل'); contact_address_label=models.CharField(max_length=80,default='آدرس دفتر'); contact_cta_eyebrow=models.CharField(max_length=120,default='نیاز به پیدا کردن ملک دارید؟'); contact_cta_title=models.CharField(max_length=180,default='از بین ملک‌های موجود شروع کنید.'); contact_cta_button=models.CharField(max_length=100,default='مشاهده املاک')
    footer_copyright=models.CharField(max_length=180,default='© ۱۴۰۵ — تمامی حقوق محفوظ است.'); footer_office_empty_text=models.CharField(max_length=180,default='اطلاعات دفتر در حال تکمیل است.'); instagram_url=models.URLField(blank=True); telegram_url=models.URLField(blank=True); whatsapp_url=models.URLField(blank=True); instagram_label=models.CharField(max_length=60,default='اینستاگرام'); telegram_label=models.CharField(max_length=60,default='تلگرام'); whatsapp_label=models.CharField(max_length=60,default='واتساپ'); updated_at=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
        if not self.pk and SiteSettings.objects.exists(): self.pk=SiteSettings.objects.first().pk
        super().save(*args,**kwargs)
    def clean(self):
        from django.core.exceptions import ValidationError
        from django.core.validators import URLValidator
        import re
        for field in ('primary_color','secondary_color','background_color','text_color','accent_color','line_color'):
            if not re.fullmatch(r'#[0-9A-Fa-f]{6}',getattr(self,field) or ''): raise ValidationError({field:'رنگ باید به صورت HEX شش‌رقمی باشد؛ مثل #B8945C.'})
        for field in ('logo','hero_image'):
            value=getattr(self,field)
            if value:
                if value.size>5*1024*1024: raise ValidationError({field:'حجم تصویر نباید بیشتر از ۵ مگابایت باشد.'})
                if not value.name.lower().endswith('.webp'): raise ValidationError({field:'برای تصاویر تنظیمات سایت فقط فرمت WebP استفاده کنید.'})
        for field in ('instagram_url','telegram_url','whatsapp_url'):
            value=getattr(self,field)
            if value:
                try: URLValidator(schemes=['http','https'])(value)
                except ValidationError: raise ValidationError({field:'آدرس باید یک لینک معتبر HTTP یا HTTPS باشد.'})
    class Meta:
        verbose_name='تنظیمات ظاهری سایت'; verbose_name_plural='تنظیمات ظاهری سایت'
