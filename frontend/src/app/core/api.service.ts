import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';
import { environment } from '../../environments/environment';
export interface PropertyImage {id:number; property?:number; image_url:string|null; caption?:string; sort_order:number;}
export interface Property {id?:number;slug:string;title:string;deal_type:string;property_type:string;city:string;district:string;address?:string;area:number;bedrooms:number;floor?:string;built_year?:number;price:number;deposit:number;rent:number;status:string;featured:boolean;image_url:string|null;agent_name:string|null;agent_phone?:string;agent?:number|null;parking:boolean;elevator:boolean;storage:boolean;balcony:boolean;description?:string;gallery?:PropertyImage[];}
export interface Agent {id:number;name:string;role:string;phone:string;bio:string;image_url:string|null;is_active?:boolean;}
@Injectable({providedIn:'root'}) export class ApiService {
 private http=inject(HttpClient); private auth=inject(AuthService); private base=environment.apiUrl;
 private headers(){return this.auth.token()?new HttpHeaders({Authorization:`Token ${this.auth.token()}`}):undefined;}
 list<T>(value:any):T[]{return Array.isArray(value)?value:(value?.results ?? []);}
 properties(filters:Record<string,string>={}){let p=new HttpParams();Object.entries(filters).forEach(([k,v])=>{if(v)p=p.set(k,v)});return this.http.get<any>(`${this.base}/properties/`,{params:p});}
 property(slug:string){return this.http.get<Property>(`${this.base}/properties/${slug}/`);}
 createProperty(data:FormData){return this.http.post<Property>(`${this.base}/properties/`,data,{headers:this.headers()});}
 updateProperty(slug:string,data:FormData){return this.http.patch<Property>(`${this.base}/properties/${slug}/`,data,{headers:this.headers()});}
 deleteProperty(slug:string){return this.http.delete(`${this.base}/properties/${slug}/`,{headers:this.headers()});}
 propertyImages(property:number){return this.http.get<any>(`${this.base}/property-images/`,{params:new HttpParams().set('property',property),headers:this.headers()});}
 addPropertyImage(property:number,file:File,sortOrder=0){const fd=new FormData();fd.append('property',String(property));fd.append('image',file);fd.append('sort_order',String(sortOrder));return this.http.post<PropertyImage>(`${this.base}/property-images/`,fd,{headers:this.headers()});}
 deletePropertyImage(id:number){return this.http.delete(`${this.base}/property-images/${id}/`,{headers:this.headers()});}
 agents(){return this.http.get<any>(`${this.base}/agents/`);}
 createAgent(data:FormData){return this.http.post<Agent>(`${this.base}/agents/`,data,{headers:this.headers()});}
 updateAgent(id:number,data:FormData){return this.http.patch<Agent>(`${this.base}/agents/${id}/`,data,{headers:this.headers()});}
 deleteAgent(id:number){return this.http.delete(`${this.base}/agents/${id}/`,{headers:this.headers()});}
 leads(){return this.http.get<any>(`${this.base}/leads/manage/`,{headers:this.headers()});}
 updateLead(id:number,data:any){return this.http.patch(`${this.base}/leads/${id}/`,data,{headers:this.headers()});}
 leadActivities(lead:number){return this.http.get<any>(`${this.base}/lead-activities/`,{params:new HttpParams().set('lead',lead),headers:this.headers()});}
 createLeadActivity(data:any){return this.http.post(`${this.base}/lead-activities/`,data,{headers:this.headers()});}
 office(){return this.http.get<any>(`${this.base}/office/`);}
 updateOffice(data:any){return this.http.put(`${this.base}/office/`,data,{headers:this.headers()});}
 dashboard(){return this.http.get<any>(`${this.base}/dashboard/`,{headers:this.headers()});}
 analytics(){return this.http.get<any>(`${this.base}/analytics/`,{headers:this.headers()});}
 favorites(){return this.http.get<Array<{property_slug:string;property_id:number}>>(`${this.base}/favorites/`,{headers:this.headers()});}
 addFavorite(slug:string){return this.http.post(`${this.base}/favorites/`,{property_slug:slug},{headers:this.headers()});}
 removeFavorite(slug:string){return this.http.delete(`${this.base}/favorites/${encodeURIComponent(slug)}/`,{headers:this.headers()});}
 lead(data:unknown):Observable<unknown>{return this.http.post(`${this.base}/leads/`,data);}
}
