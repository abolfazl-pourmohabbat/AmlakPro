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
  `,
  styles:[`
    .info-page{min-height:calc(100vh - 82px);background:#f1eee8;padding-bottom:90px}.info-hero{padding:90px 7vw 55px;background:#ebe7df}.info-hero h1{font-size:48px;margin:12px 0}.info-hero p{color:#777;line-height:2}.info-content{width:min(1000px,86vw);margin:0 auto;padding-top:55px}.info-content article{background:#fff;padding:38px}.info-content h2{font-size:28px;margin-top:0}.info-content p{color:#666;line-height:2.2;font-size:14px}.info-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:18px 0}.info-cards div{background:#fff;padding:25px;border-top:2px solid #b8945c}.info-cards strong,.info-cards span{display:block}.info-cards span{font-size:12px;color:#888;margin-top:8px}.info-button{display:inline-block;background:#171714;color:#fff;padding:13px 22px;margin-top:8px}@media(max-width:700px){.info-hero{padding:60px 22px 40px}.info-hero h1{font-size:36px}.info-content{width:auto;margin:0 22px}.info-cards{grid-template-columns:1fr}}
  `]
})
export class AboutComponent {}
