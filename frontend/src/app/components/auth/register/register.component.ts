import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../services/auth.service';

/**
 * Register Component
 * Handles new user registration
 */
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  loading = false;
  submitted = false;
  error: string | null = null;
  success: string | null = null;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Redirect to dashboard if already logged in
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
      return;
    }

    this.initializeForm();
  }

  /**
   * Initialize register form with validation
   */
  initializeForm(): void {
    this.registerForm = this.formBuilder.group(
      {
        username: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(100)]],
        email: ['', [Validators.required, Validators.email]],
        password: ['', [Validators.required, Validators.minLength(6), Validators.maxLength(255)]],
        confirmPassword: ['', Validators.required]
      },
      { validators: this.passwordMatchValidator }
    );
  }

  /**
   * Custom validator to check if passwords match
   */
  passwordMatchValidator(group: AbstractControl): ValidationErrors | null {
    const password = group.get('password')?.value;
    const confirmPassword = group.get('confirmPassword')?.value;

    if (password && confirmPassword && password !== confirmPassword) {
      group.get('confirmPassword')?.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }

    if (password && confirmPassword && password === confirmPassword) {
      group.get('confirmPassword')?.setErrors(null);
    }

    return null;
  }

  /**
   * Convenience getter for form controls
   */
  get f() {
    return this.registerForm.controls;
  }

  /**
   * Handle form submission
   */
  onSubmit(): void {
    this.submitted = true;
    this.error = null;
    this.success = null;

    // Stop if form is invalid
    if (this.registerForm.invalid) {
      return;
    }

    this.loading = true;
    const { username, email, password } = this.registerForm.value;

    this.authService.register(username, email, password).subscribe({
      next: (response: any) => {
        console.log('Registration successful:', response);
        this.loading = false;
        this.success = 'Account created successfully! Redirecting to login...';

        // Redirect to login after 2 seconds
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 2000);
      },
      error: (error: any) => {
        console.error('Registration error:', error);
        this.loading = false;
        this.error = error.error?.message || 'Registration failed. Please try again.';
      }
    });
  }

  /**
   * Clear error message
   */
  clearError(): void {
    this.error = null;
  }
}
