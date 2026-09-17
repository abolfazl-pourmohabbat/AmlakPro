import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  standalone: true,
  imports: [RouterLink],
  template: `
    <section class="info-page">
      <div class="info-hero"><span class="eyebrow dark">ABOUT AMLAKPRO</span><h1>درباره ما</h1><p>کنار شما هستیم تا پیدا کردن خانه مناسب، ساده‌تر و مطمئن‌تر باشد.</p></div>
      <div class="info-content">
        <article><h2>املاک پرو</h2><p>ما یک دفتر املاک با تمرکز روی معرفی فایل‌های واقعی، اطلاعات شفاف و ارتباط مستقیم با مشاوران هستیم. هدف ما این است که انتخاب ملک برای شما تجربه‌ای ساده و حرفه‌ای باشد.</p></article>
        <div class="info-cards"><div><strong>فایل‌های متنوع</strong><span>فروش، رهن و اجاره</span></div><div><strong>مشاوران متخصص</strong><span>برای انتخاب بهتر</span></div><div><strong>پشتیبانی</strong><span>در مسیر خرید و اجاره</span></div></div>
        <a routerLink="/contact" class="info-button">تماس با ما</a>
      </div>
    </section>
  `
})
export class AboutComponent {}
