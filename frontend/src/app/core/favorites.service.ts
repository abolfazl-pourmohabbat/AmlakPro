import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';
import { catchError, finalize, of } from 'rxjs';

const GUEST_KEY = 'amlakpro.favorite-slugs.guest';

@Injectable({providedIn: 'root'})
export class FavoritesService {
  private http = inject(HttpClient);
  private auth = inject(AuthService);
  private values = new Set<string>(this.read(GUEST_KEY));
  private base = environment.apiUrl;
  private accountKey: string | null = null;
  private syncing = false;

  private read(key: string): string[] {
    try {
      const parsed = JSON.parse(localStorage.getItem(key) || '[]');
      return Array.isArray(parsed) ? parsed.filter(value => typeof value === 'string') : [];
    } catch {
      return [];
    }
  }

  private persist() {
    localStorage.setItem(this.accountKey || GUEST_KEY, JSON.stringify([...this.values]));
  }

  private accountStorageKey(userId: number) {
    return `amlakpro.favorite-slugs.user.${userId}`;
  }

  has(slug: string) { return this.values.has(slug); }

  toggle(slug: string) {
    const active = this.values.has(slug);
    if (active) this.values.delete(slug); else this.values.add(slug);
    this.persist();

    if (this.auth.loggedIn()) {
      const request = active
        ? this.http.delete(`${this.base}/favorites/${encodeURIComponent(slug)}/`, {headers:this.auth.headers()})
        : this.http.post(`${this.base}/favorites/`, {property_slug:slug}, {headers:this.auth.headers()});
      request.pipe(catchError(() => of(null))).subscribe();
    }
    return !active;
  }

  all() { return [...this.values]; }
  count() { return this.values.size; }

  syncWithAccount() {
    if (!this.auth.loggedIn() || this.syncing) return;
    this.syncing = true;
    const guestSlugs = this.read(GUEST_KEY);

    this.auth.me().pipe(
      catchError(() => of(null)),
      finalize(() => this.syncing = false)
    ).subscribe(user => {
      if (!user) return;
      this.accountKey = this.accountStorageKey(user.id);
      const cachedAccount = new Set(this.read(this.accountKey));
      guestSlugs.forEach(slug => cachedAccount.add(slug));

      this.http.get<Array<{property_slug:string}>>(`${this.base}/favorites/`, {headers:this.auth.headers()}).pipe(
        catchError(() => of([]))
      ).subscribe(serverItems => {
        const serverSlugs = new Set(serverItems.map(item => item.property_slug));
        const missingFromServer = [...cachedAccount].filter(slug => !serverSlugs.has(slug));

        missingFromServer.forEach(slug => {
          this.http.post(`${this.base}/favorites/`, {property_slug:slug}, {headers:this.auth.headers()})
            .pipe(catchError(() => of(null))).subscribe();
          serverSlugs.add(slug);
        });

        this.values = serverSlugs;
        this.persist();
        localStorage.removeItem(GUEST_KEY);
      });
    });
  }

  resetAfterLogout() {
    this.accountKey = null;
    this.values = new Set(this.read(GUEST_KEY));
  }
}
