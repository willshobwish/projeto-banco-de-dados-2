import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
@Component({
  selector: 'app-upload',
  templateUrl: './upload.page.html',
  styleUrls: ['./upload.page.scss'],
})
export class UploadPage {
  fileUploadForm: FormGroup;

  constructor(private formBuilder: FormBuilder) {
    this.fileUploadForm = this.formBuilder.group({
      file: [null, Validators.required], // Add validation if needed
    });
  }

  onFileChange(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.fileUploadForm.patchValue({
        file: file,
      });
    }
  }

  onSubmit() {
    if (this.fileUploadForm.valid) {
      const formData = new FormData();
      formData.append('file', this.fileUploadForm.get('file')?.value);

      // Here you can send formData to your backend API
      console.log('File uploaded:', this.fileUploadForm.get('file')?.value);
    }
  }
}
