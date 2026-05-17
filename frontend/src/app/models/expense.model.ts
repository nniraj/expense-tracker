/**
 * Expense Model
 * Represents an expense record in the application
 */
export interface Expense {
  id?: number;
  description: string;
  amount: number;
  category_id?: number;
  user_id?: number;
  date?: Date | string;
  category?: { id: number; name: string };
}

/**
 * Expense Response from API
 */
export interface ExpenseResponse {
  id: number;
  description: string;
  amount: number;
  category_id: number | null;
  user_id: number;
  date: string;
}
