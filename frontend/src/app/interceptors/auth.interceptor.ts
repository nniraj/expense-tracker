import { inject } from '@angular/core';
import {
  HttpInterceptorFn,
  HttpErrorResponse
} from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { StorageService } from '../services/storage.service';

/**
 * Auth Interceptor (Functional)
 * Automatically adds JWT token to all HTTP requests
 * Handles 401 errors by redirecting to login
 */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
      console.log('AUTH INTERCEPTOR EXECUTED');
  const storageService = inject(StorageService);
  const authService = inject(AuthService);
  
  const token = storageService.getToken();
  console.log('TOKEN:', token);

  if (token) {
    // Add Authorization header with JWT token
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        // Token expired or invalid
console.error('401 Unauthorized', error);
authService.logout();
console.log('Interceptor token:', token);
console.log('Request URL:', req.url);
      }
      return throwError(() => error);
    })
  );
};

