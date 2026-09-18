from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SiteSettings
class SiteSettingsSerializer(serializers.ModelSerializer):
    logo_url=serializers.SerializerMethodField(); hero_image_url=serializers.SerializerMethodField()
    class Meta: model=SiteSettings; fields='__all__'; read_only_fields=['id','logo_url','hero_image_url','updated_at']
    def _url(self,obj,field):
        value=getattr(obj,field)
        if not value:return None
        request=self.context.get('request'); return request.build_absolute_uri(value.url) if request else value.url
    def get_logo_url(self,obj): return self._url(obj,'logo')
    def get_hero_image_url(self,obj): return self._url(obj,'hero_image')
class SiteSettingsView(APIView):
    def get(self,request):
        settings=SiteSettings.objects.first() or SiteSettings.objects.create()
        return Response(SiteSettingsSerializer(settings,context={'request':request}).data)
    def put(self,request):
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser): return Response({'detail':'دسترسی غیرمجاز'},status=403)
        settings=SiteSettings.objects.first() or SiteSettings.objects.create(); serializer=SiteSettingsSerializer(settings,data=request.data,partial=True,context={'request':request}); serializer.is_valid(raise_exception=True); serializer.save(); return Response(serializer.data)
