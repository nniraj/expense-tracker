import { Injectable } from '@angular/core';
import { User } from '../models/user.model';

/**
 * Storage Service
 * Manages localStorage operations for token and user data
 */
@Injectable({
  providedIn: 'root'
})
export class StorageService {
  private readonly TOKEN_KEY = 'auth_token';
  private readonly USER_KEY = 'current_user';

  /**
   * Set authentication token
   * @param token JWT token
   */
  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  /**
   * Get authentication token
   * @returns JWT token or null
   */
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Clear authentication token
   */
  clearToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  /**
   * Set current user data
   * @param user User object
   */
  setUser(user: User): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
  }

  /**
   * Get current user data
   * @returns User object or null
   */
  getUser(): User | null {
    const userStr = localStorage.getItem(this.USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  }

  /**
   * Clear user data
   */
  clearUser(): void {
    localStorage.removeItem(this.USER_KEY);
  }

  /**
   * Clear all storage
   */
  clearAll(): void {
    localStorage.clear();
  }

  /**
   * Check if token exists
   * @returns True if token exists
   */
  hasToken(): boolean {
    return !!localStorage.getItem(this.TOKEN_KEY);
  }
}
