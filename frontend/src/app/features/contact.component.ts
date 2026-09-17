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
  `
})
export class ContactComponent {
  private api=inject(ApiService); office:any={};
  ngOnInit(){this.api.office().subscribe({next:v=>this.office=v});}
}
