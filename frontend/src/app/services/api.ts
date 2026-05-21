import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  pingBackend() {
    return this.http.get(`${this.baseUrl}/test/ping`);
  }
  getExpenses(): Observable<any> {
    return this.http.get(`${this.baseUrl}/expenses`);
  }
}