import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

/**
 * Root Application Component
 * Serves as the main container for all routes
 */
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  title = 'Expense Tracker';
}
