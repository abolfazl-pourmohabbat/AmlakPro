import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';

export interface AuthUser {
  id: number;
  username: string;
  is_staff: boolean;
  is_superuser: boolean;
  name: string;
}

@Injectable({providedIn:'root'})
export class AuthService {
  private http=inject(HttpClient); private base=environment.apiUrl;
  login(username:string,password:string):Observable<{token:string}> { return this.http.post<{token:string}>(`${this.base}/auth/token/`,{username,password}).pipe(tap(r=>localStorage.setItem('amlak_token',r.token))); }
  register(data:{username:string,password:string,first_name?:string,last_name?:string,email?:string}):Observable<{token:string;name:string}> { return this.http.post<{token:string;name:string}>(`${this.base}/auth/register/`,data).pipe(tap(r=>localStorage.setItem('amlak_token',r.token))); }
  logout(){localStorage.removeItem('amlak_token');}
  token(){return localStorage.getItem('amlak_token');}
  loggedIn(){return !!this.token();}
  me():Observable<AuthUser>{return this.http.get<AuthUser>(`${this.base}/auth/me/`,{headers:this.headers()});}
  headers(){return new HttpHeaders({Authorization:`Token ${this.token()}`});}
}
