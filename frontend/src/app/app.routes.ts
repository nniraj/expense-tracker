import { Routes } from '@angular/router';
import { LoginComponent } from './components/auth/login/login.component';
import { RegisterComponent } from './components/auth/register/register.component';
import { AuthGuard } from './guards/auth.guard';

/**
 * Application Routes
 * Defines the routing structure for the Expense Tracker app
 */
export const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },

  // Public Routes (Auth)
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'register',
    component: RegisterComponent
  },

  // Protected Routes (require authentication)
  // These will be added as we create the components
  {
    path: 'dashboard',
    loadComponent: () => import('./components/dashboard/dashboard').then(m => m.DashboardComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'expenses',
    loadComponent: () => import('./components/expense/expense-list/expense-list.component').then(m => m.ExpenseListComponent),
    canActivate: [AuthGuard]
  },

  // Wildcard route for 404
  {
    path: '**',
    redirectTo: '/login'
  }
];