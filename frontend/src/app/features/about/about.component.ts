import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <section class="info-page">
      <div class="info-hero">
        <span class="eyebrow dark">شناخت بیشتر</span>
        <h1>درباره املاک پرو</h1>
        <p>یک دفتر املاک مدرن برای پیدا کردن، مقایسه و انتخاب مطمئن‌تر ملک.</p>
      </div>

      <div class="info-grid">
        <article class="info-card info-card-main">
          <span class="info-number">01</span>
          <h2>انتخاب ملک، ساده و شفاف</h2>
          <p>{{ office.description || 'در املاک پرو تلاش می‌کنیم اطلاعات ملک‌ها را روشن و کاربردی ارائه کنیم تا مسیر جست‌وجو تا معامله برای شما ساده‌تر باشد.' }}</p>
          <a routerLink="/properties" class="primary-link">مشاهده املاک</a>
        </article>
        <article class="info-card">
          <span class="info-number">02</span>
          <h2>مشاوره تخصصی</h2>
          <p>برای خرید، فروش، رهن و اجاره می‌توانید با مشاوران مجموعه در ارتباط باشید و قبل از تصمیم نهایی اطلاعات لازم را دریافت کنید.</p>
        </article>
        <article class="info-card">
          <span class="info-number">03</span>
          <h2>همراه تا معامله</h2>
          <p>هدف ما فقط نمایش یک ملک نیست؛ می‌خواهیم از اولین جست‌وجو تا بازدید و نهایی‌شدن معامله، تجربه‌ای منظم و قابل اعتماد داشته باشید.</p>
        </article>
      </div>
    </section>
  `
})
export class AboutComponent {
  private readonly api = inject(ApiService);
  protected office: any = {};

  ngOnInit(): void {
    this.api.office().subscribe({ next: value => this.office = value });
  }
}
