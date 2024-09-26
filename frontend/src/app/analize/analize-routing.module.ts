import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AnalizePage } from './analize.page';

const routes: Routes = [
  {
    path: '',
    component: AnalizePage,
    children: [
      {
        path: 'search',
        loadChildren: () =>
          import('./search/search.module').then((m) => m.SearchPageModule),
      },
      {
        path: 'upload',
        loadChildren: () =>
          import('./upload/upload.module').then((m) => m.UploadPageModule),
      },
      {
        path: 'inference',
        loadChildren: () =>
          import('./inference/inference.module').then(
            (m) => m.InferencePageModule
          ),
      },{
        path: '',
        redirectTo: 'inference',
        pathMatch: 'full'
      }
    ],
  },  {
    path: '',
    redirectTo: 'inference',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AnalizePageRoutingModule {}
