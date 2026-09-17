import {Component,inject} from '@angular/core';
import {CommonModule,NgOptimizedImage} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {ActivatedRoute,RouterLink} from '@angular/router';
import {ApiService,Property} from '../../core/api.service';
import {FavoritesService} from '../../core/favorites.service';

@Component({selector:'app-properties',standalone:true,imports:[CommonModule,FormsModule,RouterLink,NgOptimizedImage],templateUrl:'./properties.component.html'})
export class PropertiesComponent {
  api=inject(ApiService); route=inject(ActivatedRoute); favorites=inject(FavoritesService);
  items:Property[]=[]; q=''; deal=''; type=''; ordering='-featured'; loading=true; error=''; page=1; total=0; hasNext=false; hasPrevious=false;
  private lastFilterKey='';

  ngOnInit(){
    this.route.queryParams.subscribe(p=>{
      const nextQ=p['q']||'', nextDeal=p['deal_type']||'', nextType=p['property_type']||'', nextOrdering=p['ordering']||'-featured';
      const nextKey=JSON.stringify([nextQ,nextDeal,nextType,nextOrdering]);
      if(this.lastFilterKey && nextKey!==this.lastFilterKey) this.page=1;
      this.lastFilterKey=nextKey;
      this.q=nextQ; this.deal=nextDeal; this.type=nextType; this.ordering=nextOrdering;
      this.load();
    });
  }

  load(){
    this.loading=true; this.error='';
    this.api.properties({q:this.q,deal_type:this.deal,property_type:this.type,ordering:this.ordering,public:'1',page:String(this.page)}).subscribe({
      next:x=>{this.items=this.api.list<Property>(x);this.total=x?.count ?? this.items.length;this.hasNext=!!x?.next;this.hasPrevious=!!x?.previous;this.loading=false},
      error:()=>{this.items=[];this.loading=false;this.error='دریافت فهرست املاک انجام نشد.'}
    });
  }
  toggleFavorite(event: Event, slug:string){event.stopPropagation();this.favorites.toggle(slug);}
  clearFilters(){this.q='';this.deal='';this.type='';this.ordering='-featured';this.page=1;this.load();}
  nextPage(){if(this.hasNext){this.page++;this.load();}}
  previousPage(){if(this.hasPrevious){this.page--;this.load();}}
}
