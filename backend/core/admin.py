from django.contrib import admin
from .models import OfficeProfile, Agent, Property, PropertyImage, Lead, LeadActivity, Favorite

@admin.register(OfficeProfile)
class OfficeProfileAdmin(admin.ModelAdmin):
    list_display = ('name','phone','city','updated_at')

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name','role','phone','is_active')
    list_filter = ('is_active',)
    search_fields = ('name','phone')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title','deal_type','property_type','city','district','area','status','featured','agent')
    list_filter = ('deal_type','property_type','status','featured')
    search_fields = ('title','city','district','address')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property','sort_order','created_at')
    list_filter = ('property',)

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name','phone','property','status','assigned_agent','next_follow_up','created_at')
    list_filter = ('status','assigned_agent','source')
    search_fields = ('name','phone','message','notes')

@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    list_display = ('lead','activity_type','created_by','created_at')
    list_filter = ('activity_type',)
    search_fields = ('lead__name','lead__phone','text')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user','property','created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username','property__title','property__slug')
