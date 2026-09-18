from django.contrib import admin
from .models import OfficeProfile,Agent,Property,PropertyImage,Lead,LeadActivity,SiteSettings
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets=(('هویت سایت',{'fields':('site_name','site_tagline','logo','hero_image')}),('رنگ‌ها',{'fields':('primary_color','secondary_color','background_color','text_color','accent_color','line_color')}),('منوی سایت',{'fields':('nav_home','nav_properties','nav_agents','nav_about','nav_contact','nav_favorites')}),('صفحه اصلی — Hero',{'fields':('hero_eyebrow','hero_title','hero_title_emphasis','hero_description','hero_search_label','hero_search_placeholder','hero_deal_label','hero_search_button')}),('صفحه اصلی — املاک ویژه',{'fields':('featured_eyebrow','featured_title','featured_link','empty_properties_text')}),('صفحه اصلی — سه مزیت',{'fields':('trust_1_title','trust_1_text','trust_2_title','trust_2_text','trust_3_title','trust_3_text')}),('صفحه املاک',{'fields':('properties_eyebrow','properties_title','properties_intro','properties_search_placeholder','properties_deal_label','properties_type_label','properties_ordering_label','properties_apply_button','properties_clear_button','properties_prev_button','properties_next_button','properties_loading_text','properties_error_text','properties_empty_text','properties_count_label')}),('صفحه مشاوران',{'fields':('agents_eyebrow','agents_title','agents_intro','agents_empty_text','agents_phone_label')}),('صفحه درباره ما',{'fields':('about_eyebrow','about_title','about_intro','about_card_1_title','about_card_1_text','about_card_2_title','about_card_2_text','about_card_3_title','about_card_3_text','about_button')}),('صفحه تماس با ما',{'fields':('contact_eyebrow','contact_title','contact_intro','contact_office_name_label','contact_city_label','contact_description_label','contact_phone_label','contact_mobile_label','contact_address_label','contact_cta_eyebrow','contact_cta_title','contact_cta_button')}),('پاورقی و شبکه‌های اجتماعی',{'fields':('footer_copyright','footer_office_empty_text','instagram_url','instagram_label','telegram_url','telegram_label','whatsapp_url','whatsapp_label')}))
    list_display=('site_name','updated_at'); readonly_fields=('updated_at',)
    def has_add_permission(self,request): return not SiteSettings.objects.exists()
    def has_delete_permission(self,request,obj=None): return False
@admin.register(OfficeProfile)
class OfficeProfileAdmin(admin.ModelAdmin): list_display=('name','phone','city','updated_at')
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin): list_display=('name','role','phone','is_active'); list_filter=('is_active',); search_fields=('name','phone')
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin): list_display=('title','deal_type','property_type','city','district','area','status','featured','agent'); list_filter=('deal_type','property_type','status','featured'); search_fields=('title','city','district','address'); prepopulated_fields={'slug':('title',)}
@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin): list_display=('property','sort_order','created_at'); list_filter=('property',)
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin): list_display=('name','phone','property','status','assigned_agent','next_follow_up','created_at'); list_filter=('status','assigned_agent','source'); search_fields=('name','phone','message','notes')
@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin): list_display=('lead','activity_type','created_by','created_at'); list_filter=('activity_type',); search_fields=('lead__name','lead__phone','text')
