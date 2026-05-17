import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ExpenseService } from '../../../services/expense.service';
import { CategoryService } from '../../../services/category.service';
import { Expense } from '../../../models/expense.model';
import { Category } from '../../../models/category.model';

/**
 * Expense Form Component
 * Modal form for adding/editing expenses
 */
@Component({
  selector: 'app-expense-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './expense-form.component.html',
  styleUrl: './expense-form.component.css'
})
export class ExpenseFormComponent implements OnInit {
  @Input() isOpen = false;
  @Input() expense: Expense | null = null;
  @Output() close = new EventEmitter<void>();
  @Output() saved = new EventEmitter<void>();

  expenseForm!: FormGroup;
  categories: Category[] = [];
  loading = false;
  submitted = false;
  error: string | null = null;
  isEditMode = false;

  constructor(
    private formBuilder: FormBuilder,
    private expenseService: ExpenseService,
    private categoryService: CategoryService
  ) {}

  ngOnInit(): void {
    this.initializeForm();
    this.loadCategories();
  }

  /**
   * Initialize form
   */
  initializeForm(): void {
    this.expenseForm = this.formBuilder.group({
      description: ['', [Validators.required, Validators.maxLength(200)]],
      amount: ['', [Validators.required, Validators.min(0.01)]],
      category_id: [null],
      date: [new Date().toISOString().split('T')[0], Validators.required]
    });
  }

  /**
   * Load categories
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
   * Handle modal opening
   */
  ngOnChanges(): void {
    if (this.isOpen) {
      if (this.expense) {
        this.isEditMode = true;
        this.populateForm(this.expense);
      } else {
        this.isEditMode = false;
        this.initializeForm();
      }
      this.submitted = false;
      this.error = null;
    }
  }

  /**
   * Populate form with expense data
   */
  populateForm(expense: Expense): void {
    this.expenseForm.patchValue({
      description: expense.description,
      amount: expense.amount,
      category_id: expense.category_id || null,
      date: expense.date ? new Date(expense.date).toISOString().split('T')[0] : new Date().toISOString().split('T')[0]
    });
  }

  /**
   * Convenience getter
   */
  get f() {
    return this.expenseForm.controls;
  }

  /**
   * Handle form submission
   */
  onSubmit(): void {
    this.submitted = true;
    this.error = null;

    if (this.expenseForm.invalid) {
      return;
    }

    this.loading = true;
    const formValue = this.expenseForm.value;

    if (this.isEditMode && this.expense?.id) {
      // Update existing expense
      this.expenseService.updateExpense(this.expense.id, formValue).subscribe({
        next: () => {
          this.loading = false;
          this.saved.emit();
          this.closeModal();
        },
        error: (error: any) => {
          console.error('Error updating expense:', error);
          this.loading = false;
          this.error = error.error?.message || 'Failed to update expense. Please try again.';
        }
      });
    } else {
      // Create new expense
      this.expenseService.createExpense(formValue).subscribe({
        next: () => {
          this.loading = false;
          this.saved.emit();
          this.closeModal();
        },
        error: (error: any) => {
          console.error('Error creating expense:', error);
          this.loading = false;
          this.error = error.error?.message || 'Failed to create expense. Please try again.';
        }
      });
    }
  }

  /**
   * Close modal
   */
  closeModal(): void {
    this.isOpen = false;
    this.close.emit();
  }

  /**
   * Click outside modal to close
   */
  onBackdropClick(event: MouseEvent): void {
    if (event.target === event.currentTarget) {
      this.closeModal();
    }
  }
}
