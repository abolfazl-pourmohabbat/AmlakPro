import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../core/auth.service';
import { ApiService } from '../core/api.service';

@Component({selector:'app-dashboard',standalone:true,imports:[CommonModule,FormsModule,RouterLink],templateUrl:'./dashboard.component.html'})
export class DashboardComponent{
  private http=inject(HttpClient); private auth=inject(AuthService); private api=inject(ApiService); private router=inject(Router);
  data:any=null; leads:any[]=[]; dueFollowUps:any[]=[]; login={username:'',password:''}; error=''; loading=true;
  ngOnInit(){this.load();}
  load(){if(!this.auth.loggedIn()){this.loading=false;return;} this.api.dashboard().subscribe({next:r=>{this.data=r;this.leads=r.recent_leads||[];this.dueFollowUps=r.due_follow_ups||[];this.loading=false},error:e=>{this.loading=false;if(e.status===401||e.status===403){this.auth.logout();}}});}
  signIn(){this.error='';this.auth.login(this.login.username,this.login.password).subscribe({next:()=>this.load(),error:()=>this.error='نام کاربری یا رمز عبور صحیح نیست.'});}
  statusLabel(s:string){return ({new:'جدید',contacted:'تماس گرفته شد',visit:'بازدید',closed:'معامله شد',cancelled:'لغو شد'} as any)[s]||s;}
  setStatus(lead:any,status:string){this.api.updateLead(lead.id,status).subscribe(()=>lead.status=status);}
  logout(){this.auth.logout();this.data=null;}
}
