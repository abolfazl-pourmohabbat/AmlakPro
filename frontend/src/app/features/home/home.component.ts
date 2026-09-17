import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgFor, NgIf, DecimalPipe, NgOptimizedImage } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { ApiService, Property } from '../../core/api.service';
import { FavoritesService } from '../../core/favorites.service';
@Component({selector:'app-home',standalone:true,imports:[FormsModule,NgFor,NgIf,DecimalPipe,RouterLink,NgOptimizedImage],templateUrl:'./home.component.html'})
export class HomeComponent {
  api=inject(ApiService); router=inject(Router); favorites=inject(FavoritesService);
  q=''; deal=''; featured:Property[]=[]; loading=true; error='';
  constructor(){
    this.api.properties({public:'1',featured:'true',page_size:'6'}).subscribe({
      next:x=>{this.featured=this.api.list<Property>(x).slice(0,6);this.loading=false;},
      error:()=>{this.featured=[];this.loading=false;this.error='دریافت املاک ویژه با مشکل مواجه شد. لطفاً دوباره تلاش کنید.';}
    });
  }
  toggleFavorite(event: Event, slug: string){ event.stopPropagation(); this.favorites.toggle(slug); }
  search(){this.router.navigate(['/properties'],{queryParams:{q:this.q.trim(),deal_type:this.deal}})}
}
