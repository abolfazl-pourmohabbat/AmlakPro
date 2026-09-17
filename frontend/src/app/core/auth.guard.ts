import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { catchError, map, of } from 'rxjs';
import { AuthService } from './auth.service';

export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (!auth.loggedIn()) return router.createUrlTree(['/login']);
  return auth.me().pipe(
    map(user => user.is_staff || user.is_superuser ? true : router.createUrlTree(['/'])),
    catchError(() => { auth.logout(); return of(router.createUrlTree(['/login'])); })
  );
};
