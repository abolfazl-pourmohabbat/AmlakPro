from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Agent, Property, Lead, Favorite


class PropertyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff = get_user_model().objects.create_user(username='admin', password='StrongPass123!', is_staff=True)
        self.user = get_user_model().objects.create_user(username='regular', password='StrongPass123!')
        self.staff_token = Token.objects.create(user=self.staff)
        self.user_token = Token.objects.create(user=self.user)
        self.agent = Agent.objects.create(name='مشاور نمونه', phone='09120000000')
        self.property = Property.objects.create(title='آپارتمان سعادت آباد', deal_type='sale', property_type='apartment', city='تهران', district='سعادت آباد', area=120, agent=self.agent)

    def authenticate_staff(self): self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.staff_token.key}')
    def authenticate_user(self): self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')

    def test_public_property_detail(self):
        response = self.client.get(f'/api/properties/{self.property.slug}/')
        self.assertEqual(response.status_code, 200); self.assertEqual(response.data['title'], self.property.title)

    def test_closed_property_detail_is_hidden_from_public_users(self):
        self.property.status = Property.SOLD; self.property.save(update_fields=['status'])
        response = self.client.get(f'/api/properties/{self.property.slug}/')
        self.assertEqual(response.status_code, 404)

    def test_staff_can_view_closed_property_detail(self):
        self.property.status = Property.SOLD; self.property.save(update_fields=['status']); self.authenticate_staff()
        response = self.client.get(f'/api/properties/{self.property.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_property_slug_is_generated_and_unique(self):
        self.assertTrue(self.property.slug)
        duplicate = Property.objects.create(title=self.property.title, deal_type='sale', property_type='apartment', city='تهران', district='سعادت آباد', area=100)
        self.assertNotEqual(self.property.slug, duplicate.slug)

    def test_lead_can_be_created_without_auth(self):
        response = self.client.post('/api/leads/', {'name': 'علی', 'phone': '09120000000', 'property': self.property.id})
        self.assertEqual(response.status_code, 201); self.assertEqual(Lead.objects.count(), 1)

    def test_lead_rejects_invalid_phone(self):
        response = self.client.post('/api/leads/', {'name': 'علی', 'phone': 'bad', 'property': self.property.id}); self.assertEqual(response.status_code, 400)

    def test_lead_rejects_closed_property(self):
        self.property.status = Property.SOLD; self.property.save(update_fields=['status'])
        response = self.client.post('/api/leads/', {'name': 'علی', 'phone': '09120000000', 'property': self.property.id}); self.assertEqual(response.status_code, 400)

    def test_lead_rejects_past_follow_up(self):
        response = self.client.post('/api/leads/', {'name': 'علی', 'phone': '09120000000', 'property': self.property.id, 'next_follow_up': (timezone.now() - timedelta(days=1)).isoformat()}); self.assertEqual(response.status_code, 400)

    def test_property_write_requires_authentication(self):
        response = self.client.patch(f'/api/properties/{self.property.slug}/', {'title': 'تغییر'}); self.assertEqual(response.status_code, 401)

    def test_property_write_requires_staff(self):
        self.authenticate_user(); response = self.client.patch(f'/api/properties/{self.property.slug}/', {'title': 'تغییر'}); self.assertEqual(response.status_code, 403)

    def test_staff_can_update_property(self):
        self.authenticate_staff(); response = self.client.patch(f'/api/properties/{self.property.slug}/', {'title': 'عنوان جدید'}); self.assertEqual(response.status_code, 200); self.property.refresh_from_db(); self.assertEqual(self.property.title, 'عنوان جدید')

    def test_regular_user_cannot_access_dashboard(self):
        self.authenticate_user(); response = self.client.get('/api/dashboard/'); self.assertEqual(response.status_code, 403)

    def test_staff_can_access_dashboard(self):
        self.authenticate_staff(); response = self.client.get('/api/dashboard/'); self.assertEqual(response.status_code, 200); self.assertIn('properties', response.data)

    def test_auth_me_returns_current_staff(self):
        self.authenticate_staff(); response = self.client.get('/api/auth/me/'); self.assertEqual(response.status_code, 200); self.assertTrue(response.data['is_staff'])

    def test_regular_user_can_add_and_list_favorites(self):
        self.authenticate_user()
        add = self.client.post('/api/favorites/', {'property_slug': self.property.slug})
        self.assertIn(add.status_code, [200, 201]); self.assertTrue(Favorite.objects.filter(user=self.user, property=self.property).exists())
        listed = self.client.get('/api/favorites/')
        self.assertEqual(listed.status_code, 200); self.assertEqual(listed.data[0]['property_slug'], self.property.slug)

    def test_user_cannot_see_another_users_favorites(self):
        Favorite.objects.create(user=self.staff, property=self.property); self.authenticate_user()
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, 200); self.assertEqual(response.data, [])

    def test_user_can_remove_favorite(self):
        Favorite.objects.create(user=self.user, property=self.property); self.authenticate_user()
        response = self.client.delete(f'/api/favorites/{self.property.slug}/')
        self.assertEqual(response.status_code, 204); self.assertFalse(Favorite.objects.filter(user=self.user, property=self.property).exists())
