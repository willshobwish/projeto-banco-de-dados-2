import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ProcessedImagesPageRoutingModule } from './processed-images-routing.module';

import { ProcessedImagesPage } from './processed-images.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ProcessedImagesPageRoutingModule
  ],
  declarations: [ProcessedImagesPage]
})
export class ProcessedImagesPageModule {}
