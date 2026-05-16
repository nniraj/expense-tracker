import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {

  message = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {

    this.apiService.pingBackend().subscribe((res: any) => {

      console.log("API RESPONSE:", res);

      this.message = res.message;

    });

  }
}