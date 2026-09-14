from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
import re
from .models import OfficeProfile, Agent, Property, PropertyImage, Lead, LeadActivity

class OfficeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeProfile
        fields = '__all__'
        read_only_fields = ['updated_at']
class AgentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    property_count = serializers.IntegerField(source='properties.count', read_only=True)
    class Meta:
        model = Agent
        fields = '__all__'

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url

    def validate_image(self, value):
        if value:
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError('حجم تصویر نباید بیشتر از ۱۰ مگابایت باشد.')
            content_type = getattr(value, 'content_type', '')
            if content_type and content_type not in {'image/jpeg', 'image/png', 'image/webp'}:
                raise serializers.ValidationError('فرمت تصویر باید JPG، PNG یا WebP باشد.')
        return value
class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    def validate_image(self, value):
        if value:
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError('حجم تصویر نباید بیشتر از ۱۰ مگابایت باشد.')
            content_type = getattr(value, 'content_type', '')
            if content_type and content_type not in {'image/jpeg', 'image/png', 'image/webp'}:
                raise serializers.ValidationError('فرمت تصویر باید JPG، PNG یا WebP باشد.')
        return value
    class Meta:
        model = PropertyImage
        fields = ['id', 'property', 'image', 'image_url', 'caption', 'sort_order', 'created_at']
        read_only_fields = ['id', 'image_url', 'created_at']
    def get_image_url(self, obj):
        request = self.context.get('request')
        if not obj.image:
            return None
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url
class PropertySerializer(serializers.ModelSerializer):
    def validate_image(self, value):
        if value:
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError('حجم تصویر نباید بیشتر از ۱۰ مگابایت باشد.')
            content_type = getattr(value, 'content_type', '')
            if content_type and content_type not in {'image/jpeg', 'image/png', 'image/webp'}:
                raise serializers.ValidationError('فرمت تصویر باید JPG، PNG یا WebP باشد.')
        return value
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    agent_phone = serializers.CharField(source='agent.phone', read_only=True)
    image_url = serializers.SerializerMethodField()
    gallery = PropertyImageSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = '__all__'
    def get_image_url(self, obj):
        request = self.context.get('request')
        if not obj.image:
            return None
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url
class LeadSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)
    agent_name = serializers.CharField(source='assigned_agent.name', read_only=True)
    activities_count = serializers.IntegerField(source='activities.count', read_only=True)
    class Meta:
        model = Lead
        fields = ['id', 'name', 'phone', 'message', 'preferred_time', 'property', 'property_title', 'status', 'source', 'assigned_agent', 'agent_name', 'notes', 'next_follow_up', 'activities_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'property_title', 'agent_name', 'activities_count', 'created_at', 'updated_at']
    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError('نام معتبر نیست.')
        return value

    def validate_phone(self, value):
        value = re.sub(r'[\s\-()]', '', value)
        if not re.fullmatch(r'\+?\d{10,15}', value):
            raise serializers.ValidationError('شماره تماس معتبر نیست.')
        return value
    def validate_property(self, value):
        if value and value.status in {'sold', 'rented'}:
            raise serializers.ValidationError('برای این ملک امکان ثبت درخواست وجود ندارد.')
        return value

    def validate_next_follow_up(self, value):
        if value and value < timezone.now() - timedelta(minutes=1):
            raise serializers.ValidationError('زمان پیگیری نمی‌تواند در گذشته باشد.')
        return value

class LeadActivitySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    class Meta:
        model = LeadActivity
        fields = ['id', 'lead', 'activity_type', 'text', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_by_name', 'created_at']
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)
