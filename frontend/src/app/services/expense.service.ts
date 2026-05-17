import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Expense, ExpenseResponse } from '../models/expense.model';
import { Category } from '../models/category.model';

/**
 * Expense Service
 * Handles all expense-related API calls
 */
@Injectable({
  providedIn: 'root'
})
export class ExpenseService {
  private apiUrl = 'http://localhost:5000/api/expenses';

  constructor(private http: HttpClient) {}

  /**
   * Get all expenses for the current user
   * @returns Observable of expense list
   */
  getExpenses(): Observable<Expense[]> {
    return this.http.get<Expense[]>(this.apiUrl);
  }

  /**
   * Get a single expense by ID
   * @param id Expense ID
   * @returns Observable of expense
   */
  getExpense(id: number): Observable<Expense> {
    return this.http.get<Expense>(`${this.apiUrl}/${id}`);
  }

  /**
   * Create a new expense
   * @param expense Expense object to create
   * @returns Observable of response
   */
  createExpense(expense: Expense): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(this.apiUrl, expense);
  }

  /**
   * Update an existing expense
   * @param id Expense ID
   * @param expense Updated expense data
   * @returns Observable of response
   */
  updateExpense(id: number, expense: Partial<Expense>): Observable<{ msg: string }> {
    return this.http.put<{ msg: string }>(`${this.apiUrl}/${id}`, expense);
  }

  /**
   * Delete an expense
   * @param id Expense ID
   * @returns Observable of response
   */
  deleteExpense(id: number): Observable<{ msg: string }> {
    return this.http.delete<{ msg: string }>(`${this.apiUrl}/${id}`);
  }

  /**
   * Get expenses filtered by category
   * @param categoryId Category ID
   * @returns Observable of filtered expenses
   */
  getExpensesByCategory(categoryId: number): Observable<Expense[]> {
    return this.http.get<Expense[]>(`${this.apiUrl}?category_id=${categoryId}`);
  }

  /**
   * Get expenses for a specific date range
   * @param startDate Start date
   * @param endDate End date
   * @returns Observable of filtered expenses
   */
  getExpensesByDateRange(startDate: string, endDate: string): Observable<Expense[]> {
    return this.http.get<Expense[]>(`${this.apiUrl}?start_date=${startDate}&end_date=${endDate}`);
  }
}
