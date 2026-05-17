import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Category } from '../models/category.model';

/**
 * Category Service
 * Handles all category-related API calls
 */
@Injectable({
  providedIn: 'root'
})
export class CategoryService {
  private apiUrl = 'http://localhost:5000/api/categories';

  constructor(private http: HttpClient) {}

  /**
   * Get all categories
   * @returns Observable of category list
   */
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(this.apiUrl);
  }

  /**
   * Get a single category by ID
   * @param id Category ID
   * @returns Observable of category
   */
  getCategory(id: number): Observable<Category> {
    return this.http.get<Category>(`${this.apiUrl}/${id}`);
  }

  /**
   * Create a new category
   * @param category Category object to create
   * @returns Observable of response
   */
  createCategory(category: Category): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(this.apiUrl, category);
  }

  /**
   * Update an existing category
   * @param id Category ID
   * @param category Updated category data
   * @returns Observable of response
   */
  updateCategory(id: number, category: Category): Observable<{ msg: string }> {
    return this.http.put<{ msg: string }>(`${this.apiUrl}/${id}`, category);
  }

  /**
   * Delete a category
   * @param id Category ID
   * @returns Observable of response
   */
  deleteCategory(id: number): Observable<{ msg: string }> {
    return this.http.delete<{ msg: string }>(`${this.apiUrl}/${id}`);
  }
}
