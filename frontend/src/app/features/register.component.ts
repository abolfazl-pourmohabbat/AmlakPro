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
        <h1>ساخت حساب</h1>
        <p>حساب خود را بسازید تا بتوانید راحت‌تر املاک مورد علاقه‌تان را دنبال کنید.</p>
        <form (ngSubmit)="submit()">
          <div class="account-grid"><label>نام<input [(ngModel)]="first_name" name="first_name" autocomplete="given-name"></label><label>نام خانوادگی<input [(ngModel)]="last_name" name="last_name" autocomplete="family-name"></label></div>
          <label>نام کاربری<input [(ngModel)]="username" name="username" autocomplete="username" required></label>
          <label>ایمیل <small>(اختیاری)</small><input [(ngModel)]="email" name="email" type="email" autocomplete="email"></label>
          <label>رمز عبور<input [(ngModel)]="password" name="password" type="password" autocomplete="new-password" required minlength="8"></label>
          <div class="account-error" *ngIf="error">{{error}}</div>
          <button type="submit" [disabled]="loading">{{loading ? 'در حال ساخت حساب...' : 'ثبت نام'}}</button>
        </form>
        <div class="account-switch">قبلاً حساب ساخته‌اید؟ <a routerLink="/login">وارد شوید</a></div>
      </div>
    </section>
  `,
  styles: [`
    .account-page{min-height:calc(100vh - 82px);background:#f1eee8;display:grid;place-items:center;padding:70px 20px}
    .account-card{width:min(520px,100%);background:#fff;padding:44px;box-shadow:0 18px 55px #17171414}.account-card h1{font-size:34px;margin:12px 0 8px}.account-card>p{color:#777;line-height:2;font-size:13px;margin-bottom:25px}
    form{display:grid;gap:14px}.account-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}label{display:block;font-size:12px;color:#555}input{display:block;width:100%;margin-top:6px;padding:13px;border:1px solid #ddd;background:#fff;font:inherit;outline:none}input:focus{border-color:#b8945c}
    button{border:0;background:#171714;color:#fff;padding:14px;font:inherit;cursor:pointer}button:disabled{opacity:.6;cursor:wait}.account-error{color:#a33a31;background:#fff5f3;border-right:3px solid #b34c40;padding:10px;font-size:12px}.account-switch{text-align:center;margin-top:20px;color:#777;font-size:12px}.account-switch a{color:#967344;font-weight:600}
    @media(max-width:550px){.account-card{padding:30px 22px}.account-grid{grid-template-columns:1fr}}
  `]
})
export class RegisterComponent {
  private auth=inject(AuthService); private router=inject(Router);
  first_name=''; last_name=''; username=''; email=''; password=''; loading=false; error='';
  submit(){
    if(!this.username.trim() || !this.password){this.error='نام کاربری و رمز عبور را وارد کنید.';return;}
    if(this.password.length<8){this.error='رمز عبور باید حداقل ۸ کاراکتر باشد.';return;}
    this.loading=true; this.error='';
    this.auth.register({username:this.username.trim(),password:this.password,first_name:this.first_name.trim(),last_name:this.last_name.trim(),email:this.email.trim()}).subscribe({
      next:()=>this.router.navigateByUrl('/'),
      error:e=>{this.loading=false;this.error=e.error?.detail||'ثبت نام ناموفق بود. اطلاعات واردشده را بررسی کنید.';}
    });
  }
}
