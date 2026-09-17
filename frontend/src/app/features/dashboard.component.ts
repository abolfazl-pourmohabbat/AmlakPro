import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../core/auth.service';
import { ApiService } from '../core/api.service';

@Component({
  selector:'app-dashboard',
  standalone:true,
  imports:[CommonModule,FormsModule,RouterLink],
  templateUrl:'./dashboard.component.html',
  styles:[` 
    .dash-wrap{min-height:calc(100vh - 82px);display:grid;place-items:center;padding:60px 20px;background:#ece9e2}.login-card{background:#fff;width:min(440px,100%);padding:45px;box-shadow:0 20px 60px #1112}.login-card h1{font-size:32px;margin:14px 0 8px}.login-card p{color:#777;line-height:2}.login-card form{display:grid;gap:10px;margin-top:25px}.login-card input{padding:15px;border:1px solid #ddd;font:inherit;outline:none}.login-card button{padding:15px;border:0;background:#171714;color:#fff;font:inherit;cursor:pointer}.error{color:#b23b2e;display:block;min-height:22px;margin-top:10px}.back-link{display:block;margin-top:18px;color:#92713f;font-size:14px}
    .dashboard{background:#f4f1eb;min-height:calc(100vh - 82px);padding:55px 7vw 90px}.dash-top{display:flex;justify-content:space-between;align-items:end;margin-bottom:35px}.dash-top h1{font-size:40px;margin:8px 0}.dash-top p{color:#777;font-size:16px}.dash-actions{display:flex;gap:10px}.dash-actions a,.dash-actions button{border:1px solid #ccc;background:#fff;padding:12px 18px;font:inherit;cursor:pointer}.dash-actions button{background:#171714;color:#fff}.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:20px}.stat-grid article,.panel{background:#fff;padding:24px}.stat-grid small{color:#888;display:block;font-size:14px}.stat-grid strong{display:block;font-size:35px;margin:10px 0}.stat-grid span{font-size:14px;color:#987544}.dash-columns{display:grid;grid-template-columns:1.3fr .7fr;gap:20px}.panel-head{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #eee;padding-bottom:16px;margin-bottom:5px}.panel-head h2{font-size:19px;margin:0}.panel-head span,.panel-head a{font-size:14px;color:#987544}.lead{display:flex;justify-content:space-between;gap:20px;padding:18px 0;border-bottom:1px solid #eee}.lead b,.lead small{display:block}.lead b{font-size:16px}.lead small{color:#888;margin-top:4px;font-size:14px}.lead p{font-size:14px;color:#777;margin:8px 0 0}.lead select{height:40px;border:1px solid #ddd;background:#fff;padding:0 8px;font:inherit;font-size:13px}.mini-property{display:flex;gap:13px;padding:14px 0;border-bottom:1px solid #eee}.mini-photo{width:75px;height:65px;background:#ddd center/cover;flex:none}.mini-property b,.mini-property small,.mini-property span{display:block}.mini-property b{font-size:15px}.mini-property small{color:#888;font-size:13px;margin:5px 0}.mini-property span{font-size:13px;color:#987544}.empty{text-align:center;padding:35px;color:#888;font-size:15px}.follow-up-panel{margin-bottom:20px}.follow-up-badge{color:#987544;font-size:13px;white-space:nowrap}
    @media(max-width:900px){.stat-grid{grid-template-columns:repeat(2,1fr)}.dash-columns{grid-template-columns:1fr}.dash-top{display:block}.dash-actions{margin-top:20px;flex-wrap:wrap}}
    @media(max-width:550px){.dashboard{padding:35px 20px}.stat-grid{grid-template-columns:1fr}.login-card{padding:30px}.lead{display:block}.lead select{margin-top:12px;width:100%}.dash-actions a,.dash-actions button{flex:1;text-align:center}.follow-up-badge{display:block;margin-top:10px}}
  `]
})
export class DashboardComponent{
  private http=inject(HttpClient); public auth=inject(AuthService); private api=inject(ApiService); private router=inject(Router);
  data:any=null; leads:any[]=[]; dueFollowUps:any[]=[]; login={username:'',password:''}; error=''; loading=true;
  ngOnInit(){this.load();}
  load(){if(!this.auth.loggedIn()){this.loading=false;return;} this.api.dashboard().subscribe({next:r=>{this.data=r;this.leads=r.recent_leads||[];this.dueFollowUps=r.due_follow_ups||[];this.loading=false},error:e=>{this.loading=false;if(e.status===401||e.status===403){this.auth.logout();}}});}
  signIn(){this.error='';this.auth.login(this.login.username,this.login.password).subscribe({next:()=>this.load(),error:()=>this.error='نام کاربری یا رمز عبور صحیح نیست.'});}
  statusLabel(s:string){return ({new:'جدید',contacted:'تماس گرفته شد',visit:'بازدید',closed:'معامله شد',cancelled:'لغو شد'} as any)[s]||s;}
  setStatus(lead:any,status:string){this.api.updateLead(lead.id,{status}).subscribe({next:()=>lead.status=status,error:()=>{lead.status=lead.status;}});}
  logout(){this.auth.logout();this.data=null;this.router.navigateByUrl('/');}
}
