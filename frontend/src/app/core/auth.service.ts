import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';

export interface AuthUser { id:number; username:string; is_staff:boolean; is_superuser:boolean; name:string; }
const TOKEN_KEY='amlak_token';

@Injectable({providedIn:'root'})
export class AuthService {
  private http=inject(HttpClient); private base=environment.apiUrl;
  login(username:string,password:string):Observable<{token:string}>{return this.http.post<{token:string}>(`${this.base}/auth/token/`,{username,password}).pipe(tap(r=>sessionStorage.setItem(TOKEN_KEY,r.token)));}
  register(data:{username:string,password:string,first_name?:string,last_name?:string,email?:string}):Observable<{token:string;name:string}>{return this.http.post<{token:string;name:string}>(`${this.base}/auth/register/`,data).pipe(tap(r=>sessionStorage.setItem(TOKEN_KEY,r.token)));}
  logout(){sessionStorage.removeItem(TOKEN_KEY);localStorage.removeItem(TOKEN_KEY);}
  token(){
    const current=sessionStorage.getItem(TOKEN_KEY);
    if(current) return current;
    const legacy=localStorage.getItem(TOKEN_KEY);
    if(legacy){sessionStorage.setItem(TOKEN_KEY,legacy);localStorage.removeItem(TOKEN_KEY);return legacy;}
    return null;
  }
  loggedIn(){return !!this.token();}
  me():Observable<AuthUser>{return this.http.get<AuthUser>(`${this.base}/auth/me/`,{headers:this.headers()});}
  headers(){return new HttpHeaders({Authorization:`Token ${this.token()}`});}
}
