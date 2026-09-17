import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';
import { catchError, of } from 'rxjs';

const KEY = 'amlakpro.favorite-slugs';

@Injectable({providedIn: 'root'})
export class FavoritesService {
  private http = inject(HttpClient);
  private auth = inject(AuthService);
  private values = new Set<string>(this.read());
  private base = environment.apiUrl;

  private read(): string[] {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]'); }
    catch { return []; }
  }
  private persist() { localStorage.setItem(KEY, JSON.stringify([...this.values])); }
  private headers() { return new HttpHeaders({Authorization:`Token ${this.auth.token()}`}); }
  has(slug: string) { return this.values.has(slug); }
  toggle(slug: string) {
    const active = this.values.has(slug);
    if (active) this.values.delete(slug); else this.values.add(slug);
    this.persist();

    if (this.auth.loggedIn()) {
      const request = active
        ? this.http.delete(`${this.base}/favorites/${encodeURIComponent(slug)}/`, {headers:this.headers()})
        : this.http.post(`${this.base}/favorites/`, {property_slug:slug}, {headers:this.headers()});
      request.pipe(catchError(() => of(null))).subscribe();
    }
    return !active;
  }
  all() { return [...this.values]; }
  count() { return this.values.size; }

  syncWithAccount() {
    if (!this.auth.loggedIn()) return;
    this.http.get<Array<{property_slug:string}>>(`${this.base}/favorites/`, {headers:this.headers()}).subscribe({
      next: serverItems => {
        const serverSlugs = new Set(serverItems.map(item => item.property_slug));
        const localSlugs = [...this.values];
        localSlugs.forEach(slug => {
          if (!serverSlugs.has(slug)) {
            this.http.post(`${this.base}/favorites/`, {property_slug:slug}, {headers:this.headers()}).pipe(catchError(() => of(null))).subscribe();
          }
          serverSlugs.add(slug);
        });
        this.values = serverSlugs;
        this.persist();
      },
      error: () => undefined
    });
  }
}
