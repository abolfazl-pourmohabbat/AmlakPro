import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../core/auth.service';
import { FavoritesService } from '../core/favorites.service';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `<section class="account-page"><div class="account-card"><span class="eyebrow dark">AMLAKPRO ACCOUNT</span><h1>ورود به حساب</h1><p>برای ذخیره علاقه‌مندی‌ها و استفاده راحت‌تر از امکانات سایت وارد شوید.</p><form (ngSubmit)="submit()"><label>نام کاربری<input [(ngModel)]="username" name="username" autocomplete="username" required></label><label>رمز عبور<input [(ngModel)]="password" name="password" type="password" autocomplete="current-password" required></label><div class="account-error" *ngIf="error">{{error}}</div><button type="submit" [disabled]="loading">{{loading ? 'در حال ورود...' : 'ورود'}}</button></form><div class="account-switch">حساب ندارید؟ <a routerLink="/register">ثبت نام کنید</a></div></div></section>`,
  styles: [`.account-page{min-height:calc(100vh - 82px);background:#f1eee8;display:grid;place-items:center;padding:70px 20px}.account-card{width:min(480px,100%);background:#fff;padding:44px;box-shadow:0 18px 55px #17171414}.account-card h1{font-size:34px;margin:12px 0 8px}.account-card>p{color:#777;line-height:2;font-size:15px;margin-bottom:25px}form{display:grid;gap:14px}label{display:block;font-size:14px;color:#555}input{display:block;width:100%;margin-top:6px;padding:13px;border:1px solid #ddd;background:#fff;font:inherit;outline:none}input:focus{border-color:#b8945c}button{border:0;background:#171714;color:#fff;padding:14px;font:inherit;cursor:pointer}button:disabled{opacity:.6;cursor:wait}.account-error{color:#a33a31;background:#fff5f3;border-right:3px solid #b34c40;padding:10px;font-size:14px}.account-switch{text-align:center;margin-top:20px;color:#777;font-size:14px}.account-switch a{color:#967344;font-weight:600}@media(max-width:550px){.account-card{padding:30px 22px}}`]
})
export class LoginComponent {
  private auth=inject(AuthService); private favorites=inject(FavoritesService); private router=inject(Router);
  username=''; password=''; loading=false; error='';
  submit(){
    if(!this.username.trim() || !this.password){this.error='نام کاربری و رمز عبور را وارد کنید.';return;}
    this.loading=true; this.error='';
    this.auth.login(this.username.trim(),this.password).subscribe({next:()=>{this.favorites.syncWithAccount();this.router.navigateByUrl('/')},error:e=>{this.loading=false;this.error=e.error?.non_field_errors?.[0]||e.error?.detail||'ورود ناموفق بود. نام کاربری یا رمز عبور را بررسی کنید.';}});
  }
}
