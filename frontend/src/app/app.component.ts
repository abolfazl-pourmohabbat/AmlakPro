import { Component, inject } from '@angular/core';
import { NavigationEnd, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs';
import { ApiService } from './core/api.service';
import { AuthService } from './core/auth.service';
import { FavoritesService } from './core/favorites.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.component.html',
  styles: [`
    .nav{gap:22px}
    .nav nav{flex:1;justify-content:center;align-items:center;gap:26px}
    .nav-account{display:flex;align-items:center;gap:7px;white-space:nowrap}
    .nav-account a{font-size:13px}
    .nav-favorites{color:#d7d5ce;padding:9px 10px}
    .nav-favorites:hover{color:#fff}
    .nav-register{border:1px solid #80683f;color:#d5b577;padding:9px 13px}
    .nav-login{background:#c6a66e;color:#111;padding:10px 15px}
    .nav-register:hover{background:#c6a66e;color:#111}
    .nav-login:hover{background:#d7b77c}
    .staff-links{display:flex;align-items:center;gap:5px;border-right:1px solid #383632;padding-right:8px;margin-right:2px}
    .staff-links a{color:#d7d5ce;padding:8px 8px}
    .staff-links a:hover,.staff-links a.active{color:#d5b577}
    .nav-logout{border:0;background:transparent;color:#aaa;padding:8px;cursor:pointer;font:inherit}
    .nav-mobile-account{display:none}
    @media(max-width:1180px){.nav{gap:12px}.nav nav{gap:17px}.nav-account{gap:3px}.nav-account a{font-size:12px}.nav-register,.nav-login{padding:8px 9px}.staff-links a{padding:7px 5px}}
    @media(max-width:800px){
      .nav{gap:0;position:relative}
      .nav nav{justify-content:flex-start}
      .nav-account{display:none}
      .nav-mobile-account{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;padding:12px 16px;border-top:1px solid #2b2a27;margin-top:10px}
      .nav-mobile-account a,.nav-mobile-account button{display:block;text-align:center;padding:10px 6px;font-size:13px}
      .nav-mobile-account .nav-register{border:1px solid #80683f;color:#d5b577}
      .nav-mobile-account .nav-login{background:#c6a66e;color:#111}
      .nav-mobile-staff{grid-column:1/-1;display:grid;grid-template-columns:repeat(3,1fr);gap:6px;padding-bottom:4px}
      .nav-mobile-staff a{border:1px solid #33302b;color:#d7d5ce}
      .nav-mobile-staff .active{color:#d5b577;border-color:#80683f}
      .nav-mobile-logout{grid-column:1/-1;border:1px solid #33302b;background:transparent;color:#bbb}
    }
  `]
})
export class AppComponent {
  protected readonly api = inject(ApiService);
  protected readonly auth = inject(AuthService);
  protected readonly favorites = inject(FavoritesService);
  protected readonly router = inject(Router);
  protected office: any = {};
  protected menuOpen = false;
  protected isStaff = false;

  ngOnInit(): void {
    this.api.office().subscribe({ next: (value) => (this.office = value) });
    this.refreshAccountState();
    this.router.events.pipe(filter(event => event instanceof NavigationEnd)).subscribe(() => this.refreshAccountState());
  }

  private refreshAccountState(): void {
    if (!this.auth.loggedIn()) { this.isStaff = false; return; }
    this.auth.me().subscribe({
      next: user => { this.isStaff = !!(user.is_staff || user.is_superuser); this.favorites.syncWithAccount(); },
      error: () => { this.isStaff = false; this.auth.logout(); this.favorites.resetAfterLogout(); }
    });
  }

  logout(): void {
    this.auth.logout();
    this.favorites.resetAfterLogout();
    this.isStaff = false;
    this.closeMenu();
    this.router.navigateByUrl('/');
  }

  closeMenu(): void { this.menuOpen = false; }
}
