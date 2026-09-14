import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { ApiService } from './core/api.service';
import { FavoritesService } from './core/favorites.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.component.html',
})
export class AppComponent {
  protected readonly api = inject(ApiService);
  protected readonly favorites = inject(FavoritesService);
  protected office: any = {};
  protected menuOpen = false;

  ngOnInit(): void {
    this.api.office().subscribe({ next: (value) => (this.office = value) });
  }

  closeMenu(): void {
    this.menuOpen = false;
  }
}
