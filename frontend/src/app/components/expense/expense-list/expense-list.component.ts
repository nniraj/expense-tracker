import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ExpenseService } from '../../../services/expense.service';
import { CategoryService } from '../../../services/category.service';
import { Expense } from '../../../models/expense.model';
import { Category } from '../../../models/category.model';
import { NavbarComponent } from '../../shared/navbar/navbar.component';

/**
 * Expense List Component
 * Displays all expenses in a table with pagination and filtering
 */
@Component({
  selector: 'app-expense-list',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  templateUrl: './expense-list.component.html',
  styleUrl: './expense-list.component.css'
})
export class ExpenseListComponent implements OnInit {
  expenses: Expense[] = [];
  categories: Category[] = [];
  loading = false;
  error: string | null = null;
  success: string | null = null;
  Math = Math;

  // Pagination
  currentPage = 1;
  itemsPerPage = 10;
  totalExpenses = 0;

  // Filtering & Sorting
  searchQuery = '';
  selectedCategory: number | null = null;
  sortBy: 'date' | 'amount' = 'date';
  sortOrder: 'asc' | 'desc' = 'desc';

  constructor(
    private expenseService: ExpenseService,
    private categoryService: CategoryService
  ) {}

  ngOnInit(): void {
    this.loadCategories();
    this.loadExpenses();
  }

  /**
   * Load all categories for filter dropdown
   */
  loadCategories(): void {
    this.categoryService.getCategories().subscribe({
      next: (data: Category[]) => {
        this.categories = data;
      },
      error: (error: any) => {
        console.error('Error loading categories:', error);
      }
    });
  }

  /**
   * Load expenses from API
   */
  loadExpenses(): void {
    this.loading = true;
    this.error = null;

    this.expenseService.getExpenses().subscribe({
      next: (data: Expense[]) => {
        this.expenses = this.processExpenses(data);
        this.totalExpenses = this.expenses.length;
        this.loading = false;
      },
      error: (error: any) => {
        console.error('Error loading expenses:', error);
        this.error = 'Failed to load expenses. Please try again.';
        this.loading = false;
      }
    });
  }

  /**
   * Process expenses: filter, search, sort
   */
  processExpenses(data: Expense[]): Expense[] {
    let filtered = data;

    // Apply search filter
    if (this.searchQuery.trim()) {
      const query = this.searchQuery.toLowerCase();
      filtered = filtered.filter(
        exp => exp.description?.toLowerCase().includes(query)
      );
    }

    // Apply category filter
    if (this.selectedCategory) {
      filtered = filtered.filter(exp => exp.category_id === this.selectedCategory);
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let compareValue = 0;

      if (this.sortBy === 'date') {
        const dateA = new Date(a.date || 0).getTime();
        const dateB = new Date(b.date || 0).getTime();
        compareValue = dateA - dateB;
      } else if (this.sortBy === 'amount') {
        compareValue = (a.amount || 0) - (b.amount || 0);
      }

      return this.sortOrder === 'asc' ? compareValue : -compareValue;
    });

    return filtered;
  }

  /**
   * Get paginated expenses
   */
  get paginatedExpenses(): Expense[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    const end = start + this.itemsPerPage;
    return this.expenses.slice(start, end);
  }

  /**
   * Get total pages
   */
  get totalPages(): number {
    return Math.ceil(this.totalExpenses / this.itemsPerPage);
  }

  /**
   * Get page numbers for pagination
   */
  get pageNumbers(): number[] {
    const pages: number[] = [];
    const maxPages = 5;
    let startPage = Math.max(1, this.currentPage - Math.floor(maxPages / 2));
    let endPage = Math.min(this.totalPages, startPage + maxPages - 1);

    if (endPage - startPage + 1 < maxPages) {
      startPage = Math.max(1, endPage - maxPages + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    return pages;
  }

  /**
   * Go to specific page
   */
  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  }

  /**
   * Get category name by ID
   */
  getCategoryName(categoryId: number | null | undefined): string {
    if (!categoryId) return 'Uncategorized';
    const category = this.categories.find(c => c.id === categoryId);
    return category?.name || 'Unknown';
  }

  /**
   * Format date for display
   */
  formatDate(date: string | Date | undefined): string {
    if (!date) return '-';
    try {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch {
      return '-';
    }
  }

  /**
   * Format currency
   */
  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  }

  /**
   * Handle search
   */
  onSearch(): void {
    this.currentPage = 1;
    this.expenses = this.processExpenses(this.expenses);
  }

  /**
   * Handle filter change
   */
  onFilterChange(): void {
    this.currentPage = 1;
    this.loadExpenses();
  }

  /**
   * Handle sort change
   */
  onSortChange(): void {
    this.expenses = this.processExpenses(this.expenses);
  }

  /**
   * Delete expense
   */
  deleteExpense(id: number | undefined): void {
    if (!id) return;

    if (confirm('Are you sure you want to delete this expense?')) {
      this.expenseService.deleteExpense(id).subscribe({
        next: () => {
          this.success = 'Expense deleted successfully!';
          this.loadExpenses();
          setTimeout(() => (this.success = null), 3000);
        },
        error: (error: any) => {
          console.error('Error deleting expense:', error);
          this.error = 'Failed to delete expense. Please try again.';
        }
      });
    }
  }

  /**
   * Clear all filters
   */
  clearFilters(): void {
    this.searchQuery = '';
    this.selectedCategory = null;
    this.sortBy = 'date';
    this.sortOrder = 'desc';
    this.currentPage = 1;
    this.loadExpenses();
  }

  /**
   * Get total for displayed expenses
   */
  get displayedTotal(): number {
    return this.paginatedExpenses.reduce((sum, exp) => sum + (exp.amount || 0), 0);
  }
}
