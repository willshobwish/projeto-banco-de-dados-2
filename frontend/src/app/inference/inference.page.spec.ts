import { ComponentFixture, TestBed } from '@angular/core/testing';
import { InferencePage } from './inference.page';

describe('InferencePage', () => {
  let component: InferencePage;
  let fixture: ComponentFixture<InferencePage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(InferencePage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
