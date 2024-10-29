import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';
import { AuthGuard } from '../services/auth.guard';

const routes: Routes = [
  {
    path: 'tabs',
    component: TabsPage,
    children: [
      {
        path: 'upload',
        loadChildren: () =>
          import('../upload/upload.module').then((m) => m.UploadPageModule),
        canActivate: [AuthGuard],
      },
      {
        path: 'user',
        loadChildren: () =>
          import('../user/user.module').then((m) => m.UserPageModule),
        canActivate: [AuthGuard],
      },
      {
        path: 'report',
        loadChildren: () =>
          import('../report/report.module').then((m) => m.ReportPageModule),
        canActivate: [AuthGuard],
      },
      {
        path: '',
        redirectTo: 'report',
        pathMatch: 'full',
      },
    ],
  },
  {
    path: '',
    redirectTo: '/tabs/report',
    pathMatch: 'full',
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
})
export class TabsPageRoutingModule {}
