import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ExpenseService } from '../../services/expense.service';
import { Expense } from '../../models/expense.model';
import { NavbarComponent } from '../shared/navbar/navbar.component';

/**
 * Dashboard Component
 * Shows expense summary and recent expenses overview
 */
@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, NavbarComponent, RouterLink],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {
  expenses: Expense[] = [];
  recentExpenses: Expense[] = [];
  loading = false;

  // Summary statistics
  totalExpenses = 0;
  thisMonthExpenses = 0;
  averageExpense = 0;
  highestExpense = 0;
  expenseCount = 0;
  thisMonthCount = 0;

  constructor(private expenseService: ExpenseService) {}

  ngOnInit(): void {
    this.loadExpenses();
  }

  /**
   * Load expenses from API
   */
  loadExpenses(): void {
    this.loading = true;

    this.expenseService.getExpenses().subscribe({
      next: (data: Expense[]) => {
        this.expenses = data;
        this.calculateSummaries();
        this.recentExpenses = data.slice(0, 5);
        this.loading = false;
      },
      error: (error: any) => {
        console.error('Error loading expenses:', error);
        this.loading = false;
      }
    });
  }

  /**
   * Calculate summary statistics
   */
  calculateSummaries(): void {
    if (this.expenses.length === 0) {
      this.totalExpenses = 0;
      this.averageExpense = 0;
      this.highestExpense = 0;
      this.expenseCount = 0;
      this.thisMonthExpenses = 0;
      this.thisMonthCount = 0;
      return;
    }

    // Total expenses
    this.totalExpenses = this.expenses.reduce((sum, exp) => sum + (exp.amount || 0), 0);
    this.expenseCount = this.expenses.length;
    this.averageExpense = this.totalExpenses / this.expenseCount;
    this.highestExpense = Math.max(...this.expenses.map(exp => exp.amount || 0));

    // This month expenses
    const now = new Date();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();

    const thisMonthExp = this.expenses.filter(exp => {
      const expDate = new Date(exp.date || 0);
      return expDate.getMonth() === currentMonth && expDate.getFullYear() === currentYear;
    });

    this.thisMonthExpenses = thisMonthExp.reduce((sum, exp) => sum + (exp.amount || 0), 0);
    this.thisMonthCount = thisMonthExp.length;
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
   * Format date
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
   * Get trend indicator
   */
  getTrendIndicator(): string {
    if (this.thisMonthCount > this.expenseCount / 12) {
      return '📈 Higher than average';
    } else if (this.thisMonthCount < this.expenseCount / 12) {
      return '📉 Lower than average';
    }
    return '→ Average';
  }

  /**
   * Get month name
   */
  getCurrentMonth(): string {
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return months[new Date().getMonth()];
  }
}