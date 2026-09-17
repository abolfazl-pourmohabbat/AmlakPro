import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./features/home/home.component').then(m => m.HomeComponent) },
  { path: 'properties', loadComponent: () => import('./features/properties/properties.component').then(m => m.PropertiesComponent) },
  { path: 'properties/:slug', loadComponent: () => import('./features/properties/property-detail.component').then(m => m.PropertyDetailComponent) },
  { path: 'favorites', loadComponent: () => import('./features/favorites.component').then(m => m.FavoritesComponent) },
  { path: 'agents', loadComponent: () => import('./features/agents/agents.component').then(m => m.AgentsComponent) },
  { path: 'about', loadComponent: () => import('./features/about.component').then(m => m.AboutComponent) },
  { path: 'contact', loadComponent: () => import('./features/contact.component').then(m => m.ContactComponent) },
  { path: 'login', loadComponent: () => import('./features/login.component').then(m => m.LoginComponent) },
  { path: 'register', loadComponent: () => import('./features/register.component').then(m => m.RegisterComponent) },
  { path: 'analytics', canActivate: [authGuard], loadComponent: () => import('./features/analytics.component').then(m => m.AnalyticsComponent) },
  { path: 'dashboard', canActivate: [authGuard], loadComponent: () => import('./features/dashboard.component').then(m => m.DashboardComponent) },
  { path: 'admin', canActivate: [authGuard], loadComponent: () => import('./features/admin/admin.component').then(m => m.AdminComponent) },
  { path: 'not-found', loadComponent: () => import('./features/not-found/not-found.component').then(m => m.NotFoundComponent) },
  { path: '**', redirectTo: '/not-found' }
];
