import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { of } from 'rxjs';
import { LoginRequest, LoginResponse, RegisterRequest, User } from '../models/user.model';
import { StorageService } from './storage.service';

/**
 * Authentication Service
 * Handles user login, registration, and token management
 */
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = '/api/auth';
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser$: Observable<User | null>;

  constructor(
    private http: HttpClient,
    private storageService: StorageService
  ) {
    this.currentUserSubject = new BehaviorSubject<User | null>(
      this.storageService.getUser()
    );
    this.currentUser$ = this.currentUserSubject.asObservable();
  }

  /**
   * Get current user value
   */
  public get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  /**
   * Login user
   * @param email User email
   * @param password User password
   * @returns Observable of login response
   */
  login(email: string, password: string): Observable<LoginResponse> {
    const request: LoginRequest = { email, password };
    return this.http
      .post<LoginResponse>(`${this.apiUrl}/login`, request)
      .pipe(
        tap((response) => {
          if (response && response.token) {
            this.storageService.setToken(response.token);
            this.storageService.setUser(response.user);
            this.currentUserSubject.next(response.user);
          }
        })
      );
  }

  /**
   * Register new user
   * @param username Username
   * @param email Email address
   * @param password Password
   * @returns Observable of register response
   */
  register(username: string, email: string, password: string): Observable<any> {
    const request: RegisterRequest = { username, email, password };
    return this.http.post<any>(`${this.apiUrl}/register`, request);
  }

  /**
   * Logout current user
   */
  logout(): void {
    this.storageService.clearToken();
    this.storageService.clearUser();
    this.currentUserSubject.next(null);
  }

  /**
   * Check if user is authenticated
   * @returns True if token exists
   */
  isAuthenticated(): boolean {
    return !!this.storageService.getToken();
  }

  /**
   * Get current JWT token
   * @returns JWT token or null
   */
  getToken(): string | null {
    return this.storageService.getToken();
  }
}
