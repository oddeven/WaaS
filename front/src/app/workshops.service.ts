import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Order } from './app.component';

export const API_URL = 'http://waasapi.cfapps.io/workshops';

@Injectable()
export class WorkshopsService {

  constructor(private http: HttpClient) { }

  getPredefinedWorkshops() {
    return this.http.get(API_URL);
  }

  submitOrder(order: Order) {
    return this.http.post(API_URL, order);
  }
}
