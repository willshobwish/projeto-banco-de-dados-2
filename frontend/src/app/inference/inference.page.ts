import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/services/api.service';

@Component({
  selector: 'app-inference',
  templateUrl: './inference.page.html',
  styleUrls: ['./inference.page.scss'],
})
export class InferencePage implements OnInit {
  data: any;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.apiService.getData().subscribe(response => {
      this.data = response;
    }, error => {
      console.error('Error fetching data:', error);
    });
  }
}
