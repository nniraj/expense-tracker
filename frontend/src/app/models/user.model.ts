/**
 * User Model
 * Represents a user account
 */
export interface User {
  id?: number;
  username: string;
  email: string;
  password?: string;
}

/**
 * Login Request Payload
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Login Response from API
 */
export interface LoginResponse {
  success: boolean;
  token: string;
  user: {
    id: number;
    username: string;
    email: string;
  };
}

/**
 * Register Request Payload
 */
export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

/**
 * Register Response from API
 */
export interface RegisterResponse {
  success: boolean;
  message: string;
}
