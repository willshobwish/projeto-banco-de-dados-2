import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { InferencePageRoutingModule } from './inference-routing.module';

import { InferencePage } from './inference.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    InferencePageRoutingModule
  ],
  declarations: [InferencePage]
})
export class InferencePageModule {}
