import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  pingBackend() {
    return this.http.get(`${this.baseUrl}/test/ping`);
  }
}