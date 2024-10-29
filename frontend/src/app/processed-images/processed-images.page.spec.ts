import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ProcessedImagesPage } from './processed-images.page';

describe('ProcessedImagesPage', () => {
  let component: ProcessedImagesPage;
  let fixture: ComponentFixture<ProcessedImagesPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(ProcessedImagesPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
