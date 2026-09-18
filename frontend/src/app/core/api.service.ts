import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';
import { environment } from '../../environments/environment';
export interface PropertyImage {id:number; image_url:string|null; caption?:string; sort_order:number;}
export interface Property {id?:number;slug:string;title:string;deal_type:string;property_type:string;city:string;district:string;address?:string;area:number;bedrooms:number;floor?:string;built_year?:number;price:number;deposit:number;rent:number;status:string;featured:boolean;image_url:string|null;agent_name:string|null;agent_phone?:string;agent?:number|null;parking:boolean;elevator:boolean;storage:boolean;balcony:boolean;description?:string;gallery?:PropertyImage[];}
export interface SiteSettings {id:number;site_name:string;site_tagline:string;logo_url:string|null;hero_image_url:string|null;primary_color:string;secondary_color:string;background_color:string;text_color:string;accent_color:string;line_color:string;nav_home:string;nav_properties:string;nav_agents:string;nav_about:string;nav_contact:string;nav_favorites:string;hero_eyebrow:string;hero_title:string;hero_title_emphasis:string;hero_description:string;hero_search_label:string;hero_search_placeholder:string;hero_deal_label:string;hero_search_button:string;featured_eyebrow:string;featured_title:string;featured_link:string;empty_properties_text:string;trust_1_title:string;trust_1_text:string;trust_2_title:string;trust_2_text:string;trust_3_title:string;trust_3_text:string;about_eyebrow:string;about_title:string;about_intro:string;about_card_1_title:string;about_card_1_text:string;about_card_2_title:string;about_card_2_text:string;about_card_3_title:string;about_card_3_text:string;contact_eyebrow:string;contact_title:string;contact_intro:string;contact_phone_label:string;contact_mobile_label:string;contact_address_label:string;contact_cta_eyebrow:string;contact_cta_title:string;contact_cta_button:string;properties_eyebrow:string;properties_title:string;properties_intro:string;properties_search_placeholder:string;properties_deal_label:string;properties_type_label:string;properties_ordering_label:string;properties_apply_button:string;properties_clear_button:string;properties_prev_button:string;properties_next_button:string;properties_loading_text:string;properties_error_text:string;properties_empty_text:string;properties_count_label:string;agents_eyebrow:string;agents_title:string;agents_intro:string;agents_empty_text:string;agents_phone_label:string;about_button:string;footer_copyright:string;footer_office_empty_text:string;instagram_url:string;instagram_label:string;telegram_url:string;telegram_label:string;whatsapp_url:string;whatsapp_label:string;}
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
 agents(){return this.http.get<any>(`${this.base}/agents/`);}
 createAgent(data:FormData){return this.http.post<Agent>(`${this.base}/agents/`,data,{headers:this.headers()});}
 updateAgent(id:number,data:FormData){return this.http.patch<Agent>(`${this.base}/agents/${id}/`,data,{headers:this.headers()});}
 deleteAgent(id:number){return this.http.delete(`${this.base}/agents/${id}/`,{headers:this.headers()});}
 leads(){return this.http.get<any>(`${this.base}/leads/manage/`,{headers:this.headers()});}
 updateLead(id:number,data:any){return this.http.patch(`${this.base}/leads/${id}/`,data,{headers:this.headers()});}
 leadActivities(lead:number){return this.http.get<any>(`${this.base}/lead-activities/`,{params:new HttpParams().set('lead',lead),headers:this.headers()});}
 createLeadActivity(data:any){return this.http.post(`${this.base}/lead-activities/`,data,{headers:this.headers()});}
 office(){return this.http.get<any>(`${this.base}/office/`);}
 siteSettings(){return this.http.get<SiteSettings>(`${this.base}/site-settings/`);}
 updateOffice(data:any){return this.http.put(`${this.base}/office/`,data,{headers:this.headers()});}
 dashboard(){return this.http.get<any>(`${this.base}/dashboard/`,{headers:this.headers()});}
 analytics(){return this.http.get<any>(`${this.base}/analytics/`,{headers:this.headers()});}
 lead(data:unknown):Observable<unknown>{return this.http.post(`${this.base}/leads/`,data);}
}
