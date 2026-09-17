import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApiService } from '../core/api.service';

@Component({
  standalone: true,
  imports: [RouterLink],
  template: `
    <section class="info-page">
      <div class="info-hero"><span class="eyebrow dark">CONTACT AMLAKPRO</span><h1>تماس با ما</h1><p>برای مشاوره، بازدید یا اطلاعات بیشتر با دفتر املاک پرو در ارتباط باشید.</p></div>
      <div class="contact-grid">
        <article><span>تلفن دفتر</span><a [href]="office.phone ? 'tel:' + office.phone : null">{{office.phone || 'در حال تکمیل'}}</a></article>
        <article><span>موبایل</span><a [href]="office.mobile ? 'tel:' + office.mobile : null">{{office.mobile || 'در حال تکمیل'}}</a></article>
        <article><span>آدرس</span><p>{{office.address || 'اطلاعات آدرس در حال تکمیل است.'}}</p></article>
        <article><span>شهر</span><p>{{office.city || '—'}}</p></article>
      </div>
      <div class="contact-actions"><a routerLink="/properties">مشاهده املاک</a><a routerLink="/agents">مشاهده مشاوران</a></div>
    </section>
  `,
  styles:[`
    .info-page{min-height:calc(100vh - 82px);background:#f1eee8;padding-bottom:90px}.info-hero{padding:90px 7vw 55px;background:#ebe7df}.info-hero h1{font-size:48px;margin:12px 0}.info-hero p{color:#777;line-height:2}.contact-grid{width:min(1000px,86vw);margin:0 auto;padding:55px 0 20px;display:grid;grid-template-columns:repeat(2,1fr);gap:16px}.contact-grid article{background:#fff;padding:28px}.contact-grid span{display:block;font-size:12px;color:#967344;margin-bottom:10px}.contact-grid a{font-size:19px;font-weight:600}.contact-grid p{margin:0;color:#555;line-height:2}.contact-actions{width:min(1000px,86vw);margin:auto;display:flex;gap:10px}.contact-actions a{background:#171714;color:#fff;padding:13px 22px}@media(max-width:700px){.info-hero{padding:60px 22px 40px}.info-hero h1{font-size:36px}.contact-grid{width:auto;margin:0 22px;grid-template-columns:1fr}.contact-actions{width:auto;margin:0 22px;flex-direction:column}.contact-actions a{text-align:center}}
  `]
})
export class ContactComponent {
  private api=inject(ApiService); office:any={};
  ngOnInit(){this.api.office().subscribe({next:v=>this.office=v});}
}
