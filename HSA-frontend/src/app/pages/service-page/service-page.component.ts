import { Component, OnInit } from '@angular/core';
import {MatButtonModule } from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {TableComponentComponent} from '../../components/table-component/table-component.component';
import {Router} from '@angular/router';
import { ServiceService } from '../../services/service.service';
import { CommonModule } from '@angular/common';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';

@Component({
  selector: 'app-service-page',
  imports: [
    TableComponentComponent,
    MatButtonModule,
    MatIcon,
    CommonModule,
    LoadingFallbackComponent,
    PageTemplateComponent
  ],
  templateUrl: './service-page.component.html',
  styleUrl: './service-page.component.scss'
})
export class ServicePageComponent implements OnInit {
  services: any = null;
  serviceService: ServiceService

  constructor(private router: Router, serviceService: ServiceService, private breakpointObserver: BreakpointObserver) {
    this.serviceService = serviceService
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
    this.breakpointObserver.observe([Breakpoints.Handset]).subscribe(result => {});
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.serviceService.getService({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.services = response
      },
      error: (error) => {
      }
    })
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
