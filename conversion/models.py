from django.db import models
from django.contrib.auth import get_user_model

class ConversionTask(models.Model):
    CONVERSION_CHOICES = [
        ('pdf2docx', 'PDF to Word'),
        ('pdf2pptx', 'PDF to PowerPoint'),
        ('pdf2xlsx', 'PDF to Excel'),
        ('pdf2jpg', 'PDF to JPG'),
        ('pdf2png', 'PDF to PNG'),
        ('pdf2txt', 'PDF to TXT'),
        ('pdf2html', 'PDF to HTML'),
        ('docx2pdf', 'Word to PDF'),
        ('pptx2pdf', 'PowerPoint to PDF'),
        ('xlsx2pdf', 'Excel to PDF'),
        ('jpg2pdf', 'JPG to PDF'),
        ('png2pdf', 'PNG to PDF'),
        ('txt2pdf', 'TXT to PDF'),
        ('html2pdf', 'HTML to PDF'),
        ('merge', 'Merge PDF'),
        ('split', 'Split PDF'),
        ('compress', 'Compress PDF'),
        ('rotate', 'Rotate PDF'),
        ('edit', 'Edit PDF'),
        ('sign', 'Sign PDF'),
        ('esign', 'Convert PDF to eSign'),
        ('pdf2cad', 'PDF to CAD'),
        ('ocr', 'OCR PDF'),
        ('protect', 'Protect PDF'),
        ('unlock', 'Unlock PDF'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_file = models.FileField(upload_to='uploads/conversion/', null=True, blank=True)
    result_file = models.FileField(upload_to='results/conversion/', null=True, blank=True)
    conversion_type = models.CharField(max_length=32, choices=CONVERSION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=16, default='pending')  # pending, processing, done, failed
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_conversion_type_display()} ({self.status})"

