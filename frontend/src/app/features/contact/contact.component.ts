import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <section class="info-page contact-page">
      <div class="info-hero">
        <span class="eyebrow dark">در ارتباط باشیم</span>
        <h1>تماس با ما</h1>
        <p>برای پرسش درباره ملک‌ها، هماهنگی بازدید یا دریافت مشاوره با دفتر املاک پرو در ارتباط باشید.</p>
      </div>

      <div class="contact-grid">
        <article class="contact-card">
          <span class="contact-icon">☎</span>
          <small>تلفن دفتر</small>
          <a [href]="office.phone ? 'tel:' + office.phone : null">{{ office.phone || 'اطلاعات ثبت نشده' }}</a>
        </article>
        <article class="contact-card">
          <span class="contact-icon">◉</span>
          <small>موبایل</small>
          <a [href]="office.mobile ? 'tel:' + office.mobile : null">{{ office.mobile || 'اطلاعات ثبت نشده' }}</a>
        </article>
        <article class="contact-card">
          <span class="contact-icon">⌖</span>
          <small>آدرس دفتر</small>
          <p>{{ office.address || 'اطلاعات آدرس ثبت نشده است.' }}</p>
        </article>
      </div>

      <div class="contact-note">
        <div>
          <span class="eyebrow dark">نیاز به پیدا کردن ملک دارید؟</span>
          <h2>از بین ملک‌های موجود شروع کنید.</h2>
        </div>
        <a routerLink="/properties" class="primary-link">مشاهده املاک</a>
      </div>
    </section>
  `
})
export class ContactComponent {
  private readonly api = inject(ApiService);
  protected office: any = {};

  ngOnInit(): void {
    this.api.office().subscribe({ next: value => this.office = value });
  }
}
