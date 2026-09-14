from django.db.models import Q, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OfficeProfile, Agent, Property, PropertyImage, Lead, LeadActivity
from .serializers import OfficeProfileSerializer, AgentSerializer, PropertySerializer, PropertyImageSerializer, LeadSerializer, LeadActivitySerializer

class StaffWritePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return bool(super().has_permission(request, view) and (request.user.is_staff or request.user.is_superuser))



class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
            'name': request.user.get_full_name(),
        })

class OfficeProfileView(APIView):
    def get(self, request):
        office = OfficeProfile.objects.first() or OfficeProfile.objects.create()
        return Response(OfficeProfileSerializer(office, context={'request': request}).data)

    def put(self, request):
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            return Response({'detail': 'دسترسی غیرمجاز'}, status=403)
        office = OfficeProfile.objects.first() or OfficeProfile.objects.create()
        serializer = OfficeProfileSerializer(office, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PropertyListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'deal_type': ['exact'], 'property_type': ['exact'], 'city': ['exact', 'icontains'],
        'district': ['exact', 'icontains'], 'status': ['exact'], 'featured': ['exact'],
        'bedrooms': ['exact', 'gte'], 'area': ['gte', 'lte'], 'price': ['gte', 'lte'],
    }
    search_fields = ['title', 'city', 'district', 'address', 'description']
    ordering_fields = ['created_at', 'updated_at', 'price', 'area', 'bedrooms']
    ordering = ['-featured', '-created_at']

    def get_permissions(self):
        return [StaffWritePermission() if self.request.method == 'POST' else permissions.AllowAny()]

    def get_queryset(self):
        qs = Property.objects.select_related('agent').prefetch_related('gallery').all()
        if self.request.query_params.get('public') == '1':
            qs = qs.filter(status__in=['available', 'negotiating'])
        return qs

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.select_related('agent').prefetch_related('gallery').all()
    serializer_class = PropertySerializer
    lookup_field = 'slug'

    def get_permissions(self):
        return [StaffWritePermission() if self.request.method in ['PUT', 'PATCH', 'DELETE'] else permissions.AllowAny()]

class AgentListView(generics.ListCreateAPIView):
    queryset = Agent.objects.all().order_by('name')
    serializer_class = AgentSerializer
    search_fields = ['name', 'role', 'bio']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs if self.request.user.is_staff else qs.filter(is_active=True)

    def get_permissions(self):
        return [StaffWritePermission() if self.request.method == 'POST' else permissions.AllowAny()]

class AgentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    def get_permissions(self):
        return [StaffWritePermission() if self.request.method in ['PUT', 'PATCH', 'DELETE'] else permissions.AllowAny()]

class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'lead'

class PropertyImageListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertyImageSerializer
    filterset_fields = ['property']

    def get_queryset(self):
        return PropertyImage.objects.select_related('property').all()

    def get_permissions(self):
        return [StaffWritePermission() if self.request.method == 'POST' else permissions.AllowAny()]

class PropertyImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyImage.objects.select_related('property').all()
    serializer_class = PropertyImageSerializer
    permission_classes = [StaffWritePermission]


class LeadListView(generics.ListAPIView):
    queryset = Lead.objects.select_related('property').order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = [StaffWritePermission]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'phone', 'message']
    filterset_fields = ['status', 'property']

class LeadUpdateView(generics.UpdateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [StaffWritePermission]
    http_method_names = ['patch', 'put', 'options', 'head']

class DashboardStatsView(APIView):
    permission_classes = [StaffWritePermission]

    def get(self, request):
        props = Property.objects.select_related('agent').prefetch_related('gallery').all()
        leads = Lead.objects.all()
        return Response({
            'properties': props.count(),
            'available_properties': props.filter(status='available').count(),
            'featured_properties': props.filter(featured=True).count(),
            'agents': Agent.objects.filter(is_active=True).count(),
            'new_leads': leads.filter(status='new').count(),
            'active_leads': leads.exclude(status__in=['closed', 'cancelled']).count(),
            'closed_leads': leads.filter(status='closed').count(),
            'follow_ups': leads.filter(next_follow_up__isnull=False).count(),
            'due_follow_ups': LeadSerializer(
                leads.filter(next_follow_up__isnull=False, next_follow_up__lte=timezone.now())
                .exclude(status__in=[Lead.CLOSED, Lead.CANCELLED])
                .select_related('property', 'assigned_agent')
                .order_by('next_follow_up')[:8],
                many=True,
            ).data,
            'recent_properties': PropertySerializer(props.order_by('-created_at')[:6], many=True, context={'request': request}).data,
            'recent_leads': LeadSerializer(leads.order_by('-created_at')[:8], many=True).data,
        })


class AnalyticsView(APIView):
    permission_classes = [StaffWritePermission]

    def get(self, request):
        today = timezone.localdate()
        start = today - timedelta(days=29)
        leads = Lead.objects.all()
        props = Property.objects.all()

        daily_qs = (
            leads.filter(created_at__date__gte=start, created_at__date__lte=today)
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        daily_map = {row['day']: row['count'] for row in daily_qs}
        daily_leads = [
            {'date': start + timedelta(days=i), 'count': daily_map.get(start + timedelta(days=i), 0)}
            for i in range(30)
        ]

        property_types = [
            {'key': key, 'label': label, 'count': props.filter(property_type=key).count()}
            for key, label in Property.TYPES
        ]
        deal_types = [
            {'key': key, 'label': label, 'count': props.filter(deal_type=key).count()}
            for key, label in Property.DEAL_TYPES
        ]
        agent_rows = []
        for agent in Agent.objects.filter(is_active=True).order_by('name'):
            total = leads.filter(assigned_agent=agent).count()
            closed = leads.filter(assigned_agent=agent, status=Lead.CLOSED).count()
            agent_rows.append({
                'id': agent.id,
                'name': agent.name,
                'leads': total,
                'closed': closed,
                'conversion': round((closed / total) * 100, 1) if total else 0,
            })
        agent_rows.sort(key=lambda x: (x['closed'], x['leads']), reverse=True)

        total_leads = leads.count()
        closed = leads.filter(status=Lead.CLOSED).count()
        active = leads.exclude(status__in=[Lead.CLOSED, Lead.CANCELLED]).count()
        conversion = round((closed / total_leads) * 100, 1) if total_leads else 0

        return Response({
            'period_days': 30,
            'summary': {
                'total_leads': total_leads,
                'active_leads': active,
                'closed_leads': closed,
                'conversion_rate': conversion,
                'properties': props.count(),
                'available_properties': props.filter(status=Property.AVAILABLE).count(),
            },
            'daily_leads': daily_leads,
            'property_types': property_types,
            'deal_types': deal_types,
            'agents': agent_rows[:10],
        })


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        try:
            connection.ensure_connection()
            return Response({'status': 'ok', 'database': 'ok'})
        except Exception:
            return Response({'status': 'degraded', 'database': 'unavailable'}, status=503)


class LeadActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = LeadActivitySerializer
    permission_classes = [StaffWritePermission]

    def get_queryset(self):
        qs = LeadActivity.objects.select_related('lead', 'created_by').all()
        lead_id = self.request.query_params.get('lead')
        return qs.filter(lead_id=lead_id) if lead_id else qs

class LeadActivityDetailView(generics.DestroyAPIView):
    queryset = LeadActivity.objects.all()
    serializer_class = LeadActivitySerializer
    permission_classes = [StaffWritePermission]
