import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ProcessedImagesPage } from './processed-images.page';

const routes: Routes = [
  {
    path: '',
    component: ProcessedImagesPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ProcessedImagesPageRoutingModule {}
