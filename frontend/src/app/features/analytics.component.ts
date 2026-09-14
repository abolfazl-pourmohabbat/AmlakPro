import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../core/api.service';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-analytics', standalone: true, imports: [CommonModule, RouterLink],
  templateUrl: './analytics.component.html'
})
export class AnalyticsComponent {
  private api = inject(ApiService); private auth = inject(AuthService);
  data: any = null; loading = true; error = '';

  ngOnInit() {
    this.api.analytics().subscribe({
      next: value => { this.data = value; this.loading = false; },
      error: err => { this.loading = false; this.error = err.status === 403 ? 'دسترسی به گزارش‌ها فقط برای مدیران دفتر فعال است.' : 'گزارش‌ها بارگذاری نشد.'; }
    });
  }

  maxDaily() { return Math.max(1, ...(this.data?.daily_leads || []).map((x: any) => x.count)); }
  maxAgent() { return Math.max(1, ...(this.data?.agents || []).map((x: any) => x.leads)); }
  bar(value: number, max: number) { return `${Math.max(value ? 4 : 0, Math.round((value / max) * 100))}%`; }
  logout() { this.auth.logout(); location.href = '/'; }
}
