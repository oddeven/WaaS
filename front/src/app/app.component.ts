import { Component, OnInit } from '@angular/core';
import { WorkshopsService } from './workshops.service';

class Item {
  checked: boolean;
  name: string;
  quantity: number;
}

export class Order {
  workshopName: string = '';
  type: string = '';
  date: string;
  numberOfParticipants: number;
  items: Item[];
  additionalItems: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  order: Order;
  firstStep: boolean = true;
  secondStep: boolean = false;
  lastStep: boolean = false;
  items: any[] = [];
  predefinedWorkshops: any[];

  constructor(private workshopService: WorkshopsService) {
  }

  goToSummary() {
    this.firstStep = false;
    this.secondStep = true;

    const items = this.predefinedWorkshops[0].itemsPerParticipant;
    items.forEach(item => {
      item.quantity *= this.order.numberOfParticipants;
    });
  }

  ngOnInit(): void {
    this.workshopService.getPredefinedWorkshops().subscribe((data: any) => {
      console.log(data);
      this.predefinedWorkshops = data;
    });
    this.order = new Order();
  }

  selectType(type: string) {
    this.order.type = type;
    const workshopType = this.predefinedWorkshops.find(item => item.type === type);
    this.items = this.items.concat(workshopType.itemsPerParticipant);
    this.items = this.items.concat(workshopType.commonItems);
    this.items.forEach(item => {
      item.checked = true;
    });
  }

  submitOrder() {
    this.order.items = this.filterSelectedItems();
    console.log(this.order);
    this.workshopService.submitOrder(this.order).subscribe(res => {
        console.log('Order submitted successfully', res);
      },
      err => {
        console.log('Error occurred submitting the order', err);
      });
    this.secondStep = false;
    this.lastStep = true;
  }

  private filterSelectedItems() {
    return this.items.filter(item => item.checked);
  }

  changeQuantity(item: Item) {
    item.checked = item.quantity && item.quantity > 0;
  }
}
