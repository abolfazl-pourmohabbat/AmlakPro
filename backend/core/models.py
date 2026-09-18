from django.db import models
from django.utils.text import slugify

class OfficeProfile(models.Model):
    name=models.CharField(max_length=160,default='دفتر املاک'); name_en=models.CharField(max_length=160,default='Real Estate Office'); phone=models.CharField(max_length=30,blank=True); mobile=models.CharField(max_length=30,blank=True); address=models.CharField(max_length=300,blank=True); city=models.CharField(max_length=80,blank=True); city_en=models.CharField(max_length=80,blank=True); address_en=models.CharField(max_length=300,blank=True); description=models.TextField(blank=True); description_en=models.TextField(blank=True); updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.name
    class Meta: verbose_name='اطلاعات دفتر'; verbose_name_plural='اطلاعات دفتر'
class Agent(models.Model):
    name=models.CharField(max_length=120); name_en=models.CharField(max_length=120,blank=True); role=models.CharField(max_length=120,blank=True); role_en=models.CharField(max_length=120,blank=True); phone=models.CharField(max_length=30); bio=models.TextField(blank=True); bio_en=models.TextField(blank=True); image=models.ImageField(upload_to='agents/',blank=True,null=True); is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
class Property(models.Model):
    SALE='sale'; RENT='rent'; MORTGAGE='mortgage'; DEAL_TYPES=[(SALE,'فروش'),(RENT,'اجاره'),(MORTGAGE,'رهن')]; APARTMENT='apartment'; HOUSE='house'; VILLA='villa'; LAND='land'; COMMERCIAL='commercial'; TYPES=[(APARTMENT,'آپارتمان'),(HOUSE,'خانه'),(VILLA,'ویلا'),(LAND,'زمین'),(COMMERCIAL,'تجاری')]; AVAILABLE='available'; NEGOTIATING='negotiating'; SOLD='sold'; RENTED='rented'; STATUS=[(AVAILABLE,'موجود'),(NEGOTIATING,'در مذاکره'),(SOLD,'فروخته شد'),(RENTED,'اجاره رفت')]
    title=models.CharField(max_length=220); title_en=models.CharField(max_length=220,blank=True); slug=models.SlugField(unique=True,blank=True); deal_type=models.CharField(max_length=20,choices=DEAL_TYPES); property_type=models.CharField(max_length=20,choices=TYPES); city=models.CharField(max_length=80); city_en=models.CharField(max_length=80,blank=True); district=models.CharField(max_length=120); district_en=models.CharField(max_length=120,blank=True); address=models.CharField(max_length=300,blank=True); address_en=models.CharField(max_length=300,blank=True); area=models.PositiveIntegerField(); bedrooms=models.PositiveSmallIntegerField(default=0); floor=models.CharField(max_length=20,blank=True); built_year=models.PositiveSmallIntegerField(blank=True,null=True); price=models.DecimalField(max_digits=18,decimal_places=0,default=0); deposit=models.DecimalField(max_digits=18,decimal_places=0,default=0); rent=models.DecimalField(max_digits=18,decimal_places=0,default=0); description=models.TextField(blank=True); description_en=models.TextField(blank=True); parking=models.BooleanField(default=False); elevator=models.BooleanField(default=False); storage=models.BooleanField(default=False); balcony=models.BooleanField(default=False); featured=models.BooleanField(default=False); status=models.CharField(max_length=20,choices=STATUS,default=AVAILABLE); image=models.ImageField(upload_to='properties/',blank=True,null=True); agent=models.ForeignKey(Agent,on_delete=models.SET_NULL,null=True,blank=True,related_name='properties'); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
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
    footer_copyright=models.CharField(max_length=180,default='© ۱۴۰۵ — تمامی حقوق محفوظ است.');
    site_name_en=models.CharField(default="AmlakPro",max_length=220);
    site_tagline_en=models.CharField(default="We help you find the home you're looking for.",max_length=220);
    nav_home_en=models.CharField(default="Home",max_length=220);
    nav_properties_en=models.CharField(default="Properties",max_length=220);
    nav_agents_en=models.CharField(default="Agents",max_length=220);
    nav_about_en=models.CharField(default="About Us",max_length=220);
    nav_contact_en=models.CharField(default="Contact Us",max_length=220);
    nav_favorites_en=models.CharField(default="Favorites",max_length=220);
    hero_eyebrow_en=models.CharField(default="Specialized buying, selling and rental office",max_length=220);
    hero_title_en=models.CharField(default="The right property for you,",max_length=220);
    hero_title_emphasis_en=models.CharField(default="is right here.",max_length=220);
    hero_description_en=models.TextField(default="With precise search and professional advice, make your next property decision with confidence.");
    hero_search_label_en=models.CharField(default="Search",max_length=220);
    hero_search_placeholder_en=models.CharField(default="e.g. Saadat Abad, 120 m² apartment",max_length=220);
    hero_deal_label_en=models.CharField(default="Deal type",max_length=220);
    hero_search_button_en=models.CharField(default="Search properties",max_length=220);
    featured_eyebrow_en=models.CharField(default="Featured picks",max_length=220);
    featured_title_en=models.CharField(default="Properties worth seeing",max_length=220);
    featured_link_en=models.CharField(default="View all →",max_length=220);
    empty_properties_text_en=models.CharField(default="No featured property has been added yet.",max_length=220);
    trust_1_title_en=models.CharField(default="Transparent advice",max_length=220);
    trust_1_text_en=models.CharField(default="Clear, verifiable information for better decisions.",max_length=220);
    trust_2_title_en=models.CharField(default="Precise selection",max_length=220);
    trust_2_text_en=models.CharField(default="Useful filters to reach the right option faster.",max_length=220);
    trust_3_title_en=models.CharField(default="With you to the deal",max_length=220);
    trust_3_text_en=models.CharField(default="From the first call to viewing and closing.",max_length=220);
    about_eyebrow_en=models.CharField(default="Learn more",max_length=220);
    about_title_en=models.CharField(default="About AmlakPro",max_length=220);
    about_intro_en=models.TextField(default="A modern real estate office for finding, comparing and choosing property with confidence.");
    about_card_1_title_en=models.CharField(default="Simple and transparent",max_length=220);
    about_card_1_text_en=models.TextField(default="We present property information clearly and practically so your path from search to deal is easier.");
    about_card_2_title_en=models.CharField(default="Expert advice",max_length=220);
    about_card_2_text_en=models.TextField(default="For buying, selling, mortgage and rental, our advisors are available to provide the information you need.");
    about_card_3_title_en=models.CharField(default="With you to the deal",max_length=220);
    about_card_3_text_en=models.TextField(default="Our goal is more than displaying a property; we support you from the first search to the final deal.");
    properties_eyebrow_en=models.CharField(default="Properties",max_length=220);
    properties_title_en=models.CharField(default="Your next property",max_length=220);
    properties_intro_en=models.TextField(default="Search and filter the office's available properties.");
    properties_search_placeholder_en=models.CharField(default="City, district or property name",max_length=220);
    properties_deal_label_en=models.CharField(default="Deal type",max_length=220);
    properties_type_label_en=models.CharField(default="Property type",max_length=220);
    properties_ordering_label_en=models.CharField(default="Sort by",max_length=220);
    properties_apply_button_en=models.CharField(default="Apply filters",max_length=220);
    properties_clear_button_en=models.CharField(default="Clear",max_length=220);
    properties_prev_button_en=models.CharField(default="Previous",max_length=220);
    properties_next_button_en=models.CharField(default="Next",max_length=220);
    properties_loading_text_en=models.CharField(default="Loading properties...",max_length=220);
    properties_error_text_en=models.CharField(default="Could not load properties.",max_length=220);
    properties_empty_text_en=models.CharField(default="No property matches your search.",max_length=220);
    properties_count_label_en=models.CharField(default="properties",max_length=220);
    agents_eyebrow_en=models.CharField(default="Our team",max_length=220);
    agents_title_en=models.CharField(default="Advisors who are here for you",max_length=220);
    agents_intro_en=models.TextField(default="Local expertise, responsiveness and support through the deal.");
    agents_empty_text_en=models.CharField(default="No advisors have been added yet.",max_length=220);
    agents_phone_label_en=models.CharField(default="Contact advisor",max_length=220);
    about_button_en=models.CharField(default="View properties",max_length=220);
    contact_eyebrow_en=models.CharField(default="Let's connect",max_length=220);
    contact_title_en=models.CharField(default="Contact us",max_length=220);
    contact_intro_en=models.TextField(default="For property questions, viewing appointments or advice, contact AmlakPro.");
    contact_office_name_label_en=models.CharField(default="Office name",max_length=220);
    contact_city_label_en=models.CharField(default="City",max_length=220);
    contact_description_label_en=models.CharField(default="Office introduction",max_length=220);
    contact_phone_label_en=models.CharField(default="Office phone",max_length=220);
    contact_mobile_label_en=models.CharField(default="Mobile",max_length=220);
    contact_address_label_en=models.CharField(default="Office address",max_length=220);
    contact_cta_eyebrow_en=models.CharField(default="Looking for a property?",max_length=220);
    contact_cta_title_en=models.CharField(default="Start with the available properties.",max_length=220);
    contact_cta_button_en=models.CharField(default="View properties",max_length=220);
    footer_copyright_en=models.CharField(default="© 2026 — All rights reserved.",max_length=220);
    footer_office_empty_text_en=models.CharField(default="Office information is being completed.",max_length=220);
    instagram_label_en=models.CharField(default="Instagram",max_length=220);
    telegram_label_en=models.CharField(default="Telegram",max_length=220);
    whatsapp_label_en=models.CharField(default="WhatsApp",max_length=220); footer_office_empty_text=models.CharField(max_length=180,default='اطلاعات دفتر در حال تکمیل است.'); instagram_url=models.URLField(blank=True); telegram_url=models.URLField(blank=True); whatsapp_url=models.URLField(blank=True); instagram_label=models.CharField(max_length=60,default='اینستاگرام'); telegram_label=models.CharField(max_length=60,default='تلگرام'); whatsapp_label=models.CharField(max_length=60,default='واتساپ'); updated_at=models.DateTimeField(auto_now=True)
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
