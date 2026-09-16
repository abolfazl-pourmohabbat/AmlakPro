import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService, Agent, Property } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';

@Component({selector:'app-admin',standalone:true,imports:[CommonModule,FormsModule,RouterLink],templateUrl:'./admin.component.html'})
export class AdminComponent {
 api=inject(ApiService); auth=inject(AuthService); tab='properties'; properties:Property[]=[]; agents:Agent[]=[]; leads:any[]=[]; office:any={}; editing:Property|null=null; editingAgent:Agent|null=null; message=''; error=''; selectedLead:any=null; activities:any[]=[]; activityText=''; activityType='note';
 form:any={title:'',slug:'',deal_type:'sale',property_type:'apartment',city:'',district:'',address:'',area:100,bedrooms:2,floor:'',built_year:'',price:0,deposit:0,rent:0,status:'available',featured:false,agent:'',parking:false,elevator:false,storage:false,balcony:false,description:''};
 agentForm:any={name:'',role:'',phone:'',bio:'',is_active:true}; image:File|null=null; agentImage:File|null=null;
 ngOnInit(){if(!this.auth.loggedIn()) return; this.loadAll();}
 loadAll(){this.api.properties().subscribe(v=>this.properties=this.api.list<Property>(v));this.api.agents().subscribe(v=>this.agents=this.api.list<Agent>(v));this.api.leads().subscribe(v=>this.leads=this.api.list<any>(v));this.api.office().subscribe(v=>this.office=v);}
 selectTab(t:string){this.tab=t;this.message='';this.error='';}
 resetProperty(){this.editing=null;this.image=null;this.form={title:'',slug:'',deal_type:'sale',property_type:'apartment',city:'',district:'',address:'',area:100,bedrooms:2,floor:'',built_year:'',price:0,deposit:0,rent:0,status:'available',featured:false,agent:'',parking:false,elevator:false,storage:false,balcony:false,description:''};}
 editProperty(p:Property){this.editing=p;this.form={...p,agent:p.agent||''};window.scrollTo({top:0,behavior:'smooth'});}
 onImage(e:any){const file=e.target.files?.[0]||null;this.image=file;if(file&&file.size>4*1024*1024){this.error='حجم تصویر باید کمتر از ۴ مگابایت باشد.';this.image=null;e.target.value='';}}
 saveProperty(){const fd=new FormData();Object.entries(this.form).forEach(([k,v])=>{if(v!==null&&v!==undefined)fd.append(k,String(v));});if(this.image)fd.append('image',this.image);const req=this.editing?this.api.updateProperty(this.editing.slug,fd):this.api.createProperty(fd);req.subscribe({next:()=>{this.message='ملک با موفقیت ذخیره شد.';this.resetProperty();this.api.properties().subscribe(v=>this.properties=this.api.list<Property>(v))},error:e=>this.error=Object.values(e.error||{}).flat().join(' ')||'ذخیره ملک ناموفق بود.'});}
 removeProperty(p:Property){if(!confirm(`حذف «${p.title}»؟`))return;this.api.deleteProperty(p.slug).subscribe(()=>this.properties=this.properties.filter(x=>x.slug!==p.slug));}
 resetAgent(){this.editingAgent=null;this.agentImage=null;this.agentForm={name:'',role:'',phone:'',bio:'',is_active:true};}
 editAgent(a:Agent){this.editingAgent=a;this.agentForm={...a};window.scrollTo({top:0,behavior:'smooth'});}
 onAgentImage(e:any){const file=e.target.files?.[0]||null;this.agentImage=file;if(file&&file.size>4*1024*1024){this.error='حجم تصویر باید کمتر از ۴ مگابایت باشد.';this.agentImage=null;e.target.value='';}}
 saveAgent(){const fd=new FormData();Object.entries(this.agentForm).forEach(([k,v])=>{if(v!==null&&v!==undefined)fd.append(k,String(v));});if(this.agentImage)fd.append('image',this.agentImage);const req=this.editingAgent?this.api.updateAgent(this.editingAgent.id,fd):this.api.createAgent(fd);req.subscribe({next:()=>{this.message='مشاور با موفقیت ذخیره شد.';this.resetAgent();this.api.agents().subscribe(v=>this.agents=this.api.list<Agent>(v))},error:e=>this.error='ذخیره مشاور ناموفق بود.'});}
 removeAgent(a:Agent){if(!confirm(`حذف «${a.name}»؟`))return;this.api.deleteAgent(a.id).subscribe(()=>this.agents=this.agents.filter(x=>x.id!==a.id));}
 saveOffice(){this.api.updateOffice(this.office).subscribe({next:()=>this.message='اطلاعات دفتر ذخیره شد.',error:()=>this.error='ذخیره اطلاعات دفتر ناموفق بود.'});}
 setLeadStatus(l:any,s:string){this.api.updateLead(l.id,{status:s}).subscribe(()=>l.status=s);}
 selectLead(l:any){this.selectedLead=l;this.activityText='';this.api.leadActivities(l.id).subscribe(v=>this.activities=this.api.list<any>(v));}
 addActivity(){if(!this.selectedLead||!this.activityText.trim())return;this.api.createLeadActivity({lead:this.selectedLead.id,activity_type:this.activityType,text:this.activityText.trim()}).subscribe(()=>{this.activityText='';this.api.leadActivities(this.selectedLead.id).subscribe(v=>this.activities=this.api.list<any>(v));});}
 saveLeadDetails(){if(!this.selectedLead)return;this.api.updateLead(this.selectedLead.id,{assigned_agent:this.selectedLead.assigned_agent||null,notes:this.selectedLead.notes||'',next_follow_up:this.selectedLead.next_follow_up||null}).subscribe(()=>this.message='اطلاعات پیگیری مشتری ذخیره شد.');}
 logout(){this.auth.logout();location.href='/';}
}
