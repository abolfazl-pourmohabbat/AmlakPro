import { Injectable } from '@angular/core';

const KEY = 'amalkpro.favorite-slugs';

@Injectable({providedIn: 'root'})
export class FavoritesService {
  private values = new Set<string>(this.read());

  private read(): string[] {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]'); }
    catch { return []; }
  }
  private persist() { localStorage.setItem(KEY, JSON.stringify([...this.values])); }
  has(slug: string) { return this.values.has(slug); }
  toggle(slug: string) {
    if (this.values.has(slug)) this.values.delete(slug);
    else this.values.add(slug);
    this.persist();
    return this.values.has(slug);
  }
  all() { return [...this.values]; }
  count() { return this.values.size; }
}
