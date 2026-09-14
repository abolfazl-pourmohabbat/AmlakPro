import {Component,inject} from '@angular/core';

import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';

import {ActivatedRoute,RouterLink} from '@angular/router';
import {ApiService,Property} from '../../core/api.service';import {FavoritesService} from '../../core/favorites.service';

@Component({selector:'app-property-detail',standalone:true,imports:[CommonModule,FormsModule,RouterLink],templateUrl:'./property-detail.component.html'})
export class PropertyDetailComponent {
api=inject(ApiService); route=inject(ActivatedRoute); favorites=inject(FavoritesService); item?:Property; loading=true; selectedImage:string|null=null; submitted=false; submitting=false; error='';

lead={name:'',phone:'',preferred_time:'',message:''};

ngOnInit(){this.route.paramMap.subscribe(p=>{const slug=p.get('slug');if(slug)this.api.property(slug).subscribe({next:x=>{this.item=x;this.selectedImage=x.image_url||null;this.loading=false},error:()=>this.loading=false})})}
toggleFavorite(){if(this.item)this.favorites.toggle(this.item.slug)}
deal(v:string){return v==='sale'?'فروش':v==='rent'?'اجاره':'رهن'}

submitLead(){if(!this.item)return;this.submitting=true;this.error='';this.api.lead({...this.lead,property:this.item.id}).subscribe({next:()=>{this.submitted=true;this.submitting=false;this.lead={name:'',phone:'',preferred_time:'',message:''}},error:()=>{this.submitting=false;this.error='ارسال درخواست انجام نشد. لطفاً دوباره تلاش کنید.'}})}

}
