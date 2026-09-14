import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({providedIn:'root'})
export class AuthService {
  private http=inject(HttpClient); private base=environment.apiUrl;
  login(username:string,password:string):Observable<{token:string}> { return this.http.post<{token:string}>(`${this.base}/auth/token/`,{username,password}).pipe(tap(r=>localStorage.setItem('amlak_token',r.token))); }
  logout(){localStorage.removeItem('amlak_token');}
  token(){return localStorage.getItem('amlak_token');}
  loggedIn(){return !!this.token();}
  me():Observable<{id:number;username:string;is_staff:boolean;is_superuser:boolean;name:string}>{return this.http.get<{id:number;username:string;is_staff:boolean;is_superuser:boolean;name:string}>(`${this.base}/auth/me/`,{headers:this.headers()});}
  headers(){return new HttpHeaders({Authorization:`Token ${this.token()}`});}
}
