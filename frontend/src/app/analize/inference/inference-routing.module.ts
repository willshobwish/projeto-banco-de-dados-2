import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { InferencePage } from './inference.page';

const routes: Routes = [
  {
    path: '',
    component: InferencePage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class InferencePageRoutingModule {}
