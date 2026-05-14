import { Routes } from '@angular/router';
import { Login } from './components/login/login';
import { Dashboard } from './components/dashboard/dashboard';
import { Expense } from './components/expense/expense';

export const routes: Routes = [
  { path: '', component: Login },
  { path: 'dashboard', component: Dashboard },
  { path: 'expenses', component: Expense }
];