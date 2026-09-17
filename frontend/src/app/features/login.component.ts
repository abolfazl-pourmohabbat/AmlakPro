import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../core/auth.service';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <section class="account-page">
      <div class="account-card">
        <span class="eyebrow dark">AMLAKPRO ACCOUNT</span>
        <h1>ورود به حساب</h1>
        <p>برای ذخیره علاقه‌مندی‌ها و استفاده راحت‌تر از امکانات سایت وارد شوید.</p>
        <form (ngSubmit)="submit()">
          <label>نام کاربری<input [(ngModel)]="username" name="username" autocomplete="username" required></label>
          <label>رمز عبور<input [(ngModel)]="password" name="password" type="password" autocomplete="current-password" required></label>
          <div class="account-error" *ngIf="error">{{error}}</div>
          <button type="submit" [disabled]="loading">{{loading ? 'در حال ورود...' : 'ورود'}}</button>
        </form>
        <div class="account-switch">حساب ندارید؟ <a routerLink="/register">ثبت نام کنید</a></div>
      </div>
    </section>
  `
})
export class LoginComponent {
  private auth=inject(AuthService); private router=inject(Router);
  username=''; password=''; loading=false; error='';
  submit(){
    if(!this.username.trim() || !this.password){this.error='نام کاربری و رمز عبور را وارد کنید.';return;}
    this.loading=true; this.error='';
    this.auth.login(this.username.trim(),this.password).subscribe({
      next:()=>this.router.navigateByUrl('/'),
      error:e=>{this.loading=false;this.error=e.error?.non_field_errors?.[0]||e.error?.detail||'ورود ناموفق بود. نام کاربری یا رمز عبور را بررسی کنید.';}
    });
  }
}
