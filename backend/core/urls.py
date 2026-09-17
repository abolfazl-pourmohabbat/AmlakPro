from django.urls import path
from .views import (
    CurrentUserView, OfficeProfileView, PropertyListCreateView, PropertyDetailView,
    PropertyImageListCreateView, PropertyImageDetailView,
    AgentListView, AgentDetailView, LeadCreateView, LeadListView,
    LeadUpdateView, LeadActivityListCreateView, LeadActivityDetailView, DashboardStatsView, AnalyticsView, HealthView,
    FavoriteListView, FavoriteDetailView,
)

urlpatterns = [
    path('health/', HealthView.as_view()),
    path('auth/me/', CurrentUserView.as_view()),
    path('office/', OfficeProfileView.as_view()),
    path('properties/', PropertyListCreateView.as_view()),
    path('properties/<slug:slug>/', PropertyDetailView.as_view()),
    path('property-images/', PropertyImageListCreateView.as_view()),
    path('property-images/<int:pk>/', PropertyImageDetailView.as_view()),
    path('agents/', AgentListView.as_view()),
    path('agents/<int:pk>/', AgentDetailView.as_view()),
    path('leads/', LeadCreateView.as_view()),
    path('leads/manage/', LeadListView.as_view()),
    path('leads/<int:pk>/', LeadUpdateView.as_view()),
    path('lead-activities/', LeadActivityListCreateView.as_view()),
    path('lead-activities/<int:pk>/', LeadActivityDetailView.as_view()),
    path('favorites/', FavoriteListView.as_view()),
    path('favorites/<slug:slug>/', FavoriteDetailView.as_view()),
    path('dashboard/', DashboardStatsView.as_view()),
    path('analytics/', AnalyticsView.as_view()),
]
