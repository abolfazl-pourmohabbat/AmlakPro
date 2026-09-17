import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { ApiService } from './core/api.service';
import { FavoritesService } from './core/favorites.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.component.html',
  styles: [`
    .nav{gap:28px}
    .nav nav{flex:1;justify-content:center;align-items:center;gap:30px}
    .nav-account{display:flex;align-items:center;gap:8px;white-space:nowrap}
    .nav-account a{font-size:12px}
    .nav-favorites{color:#d7d5ce;padding:9px 10px}
    .nav-favorites:hover{color:#fff}
    .nav-register{border:1px solid #80683f;color:#d5b577;padding:9px 14px}
    .nav-login{background:#c6a66e;color:#111;padding:10px 16px}
    .nav-register:hover{background:#c6a66e;color:#111}
    .nav-login:hover{background:#d7b77c}
    @media(max-width:1050px){.nav{gap:15px}.nav nav{gap:18px}.nav-account{gap:4px}.nav-account a{font-size:11px}.nav-register,.nav-login{padding:8px 10px}}
    @media(max-width:800px){.nav-account{display:none}.nav nav{justify-content:flex-start}.nav{gap:0}}
  `]
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
