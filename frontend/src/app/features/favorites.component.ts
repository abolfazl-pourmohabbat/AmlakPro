import { Component, inject } from '@angular/core';
import { CommonModule, NgOptimizedImage } from '@angular/common';
import { RouterLink } from '@angular/router';
import { forkJoin, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { ApiService, Property } from '../core/api.service';
import { FavoritesService } from '../core/favorites.service';

@Component({
  selector: 'app-favorites',
  standalone: true,
  imports: [CommonModule, RouterLink, NgOptimizedImage],
  template: `
    <section class="favorites-page">
      <div class="favorites-head">
        <div><span class="eyebrow dark">ذخیره‌شده‌ها</span><h1>املاک موردعلاقه شما</h1></div>
        <a routerLink="/properties">← بازگشت به املاک</a>
      </div>
      <div *ngIf="loading" class="empty">در حال دریافت املاک ذخیره‌شده...</div>
      <div *ngIf="!loading && items.length" class="favorites-grid">
        <article class="property-card" *ngFor="let p of items" [routerLink]="['/properties', p.slug]">
          <div class="photo">
            <div class="photo-fallback" *ngIf="!p.image_url"></div>
            <img *ngIf="p.image_url" class="photo-img" [ngSrc]="p.image_url!" width="800" height="520" alt="تصویر ملک" loading="lazy">
            <button class="favorite-btn" type="button" (click)="remove($event,p.slug)" aria-label="حذف از علاقه‌مندی‌ها">♥</button>
            <span>{{p.deal_type==='sale'?'فروش':p.deal_type==='rent'?'اجاره':'رهن'}}</span>
          </div>
          <div class="pc-body"><small>{{p.city}}، {{p.district}}</small><h3>{{p.title}}</h3><div class="specs"><span>{{p.area}} متر</span><span>{{p.bedrooms}} خواب</span></div><strong>{{p.price ? (p.price|number) : 'تماس برای قیمت'}} تومان</strong></div>
        </article>
      </div>
      <div *ngIf="!loading && !items.length" class="favorites-empty"><h2>هنوز ملکی ذخیره نکرده‌اید</h2><p>در صفحه املاک روی ♡ بزنید تا گزینه‌های مناسب‌تان اینجا بمانند.</p><a routerLink="/properties" class="primary">مشاهده املاک</a></div>
    </section>`
})
export class FavoritesComponent {
  api = inject(ApiService); favorites = inject(FavoritesService); items: Property[] = []; loading = true;
  ngOnInit(){
    const slugs = this.favorites.all();
    if(!slugs.length){ this.loading=false; return; }
    forkJoin(slugs.map(slug => this.api.property(slug).pipe(catchError(() => of(null))))).pipe(map(items => items.filter((p): p is Property => !!p))).subscribe(items => { this.items=items; this.loading=false; });
  }
  remove(event: Event, slug: string){ event.preventDefault(); event.stopPropagation(); this.favorites.toggle(slug); this.items=this.items.filter(p=>p.slug!==slug); }
}
