import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AnalizePage } from './analize.page';

describe('AnalizePage', () => {
  let component: AnalizePage;
  let fixture: ComponentFixture<AnalizePage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(AnalizePage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
