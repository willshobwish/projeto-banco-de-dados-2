import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-image-viewer',
  templateUrl: './image-viewer.page.html',
  styleUrls: ['./image-viewer.page.scss'],
})
export class ImageViewerPage implements OnInit {
  imageUrl: string = '';

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    const imageId = this.route.snapshot.paramMap.get('imageId');
    if (imageId) {
      this.imageUrl = `http://localhost:8000/processed-images/${imageId}`;
    }
  }
}
