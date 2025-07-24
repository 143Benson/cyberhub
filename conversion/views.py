from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ConversionTaskForm
from .models import ConversionTask
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pdf2docx import Converter
from pdf2image import convert_from_path
from django.conf import settings
import os
from PIL import Image
import fitz  # PyMuPDF
import io
import traceback

def dashboard(request):
    form = ConversionTaskForm()
    # Render the correct template for the conversion dashboard
    return render(request, 'conversion/dashboard.html', {'form': form})

def convert_pdf_images_to_rgb(input_pdf_path, output_pdf_path):
    doc = fitz.open(input_pdf_path)
    for page in doc:
        img_list = page.get_images(full=True)
        for img_index, img in enumerate(img_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img_ext = base_image["ext"]
            try:
                pil_img = Image.open(io.BytesIO(image_bytes))
                if pil_img.mode != "RGB":
                    pil_img = pil_img.convert("RGB")
                buf = io.BytesIO()
                pil_img.save(buf, format=img_ext.upper())
                buf.seek(0)
                doc.update_image(xref, buf.read())
            except Exception as img_e:
                print(f"Failed to process image xref {xref}: {img_e}")
                continue  # Skip this image and continue
    doc.save(output_pdf_path)
    doc.close()

@csrf_exempt
def convert_file(request):
    # Handle file conversion logic
    if request.method == 'POST':
        form = ConversionTaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            if request.user.is_authenticated:
                task.user = request.user
            task.status = 'processing'
            task.save()
            uploaded_file = request.FILES['uploaded_file']
            conversion_type = request.POST.get('conversion_type')
            # Only implement PDF to DOCX for now
            if conversion_type == 'pdf2docx':
                try:
                    pdf_path = task.uploaded_file.path
                    # Preprocess PDF to ensure all images are RGB
                    rgb_pdf_path = pdf_path.replace('.pdf', '_rgb.pdf')
                    convert_pdf_images_to_rgb(pdf_path, rgb_pdf_path)
                    docx_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '.docx'
                    docx_path = os.path.join(settings.MEDIA_ROOT, 'results/conversion', docx_filename)
                    os.makedirs(os.path.dirname(docx_path), exist_ok=True)
                    cv = Converter(rgb_pdf_path)
                    cv.convert(docx_path, start=0, end=None)
                    cv.close()
                    # Save result file to model
                    rel_docx_path = os.path.relpath(docx_path, settings.MEDIA_ROOT)
                    task.result_file.name = rel_docx_path.replace('\\', '/')
                    # Generate thumbnail from first page
                    images = convert_from_path(rgb_pdf_path, first_page=1, last_page=1, size=(120, 120))
                    thumb_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '_thumb.jpg'
                    thumb_path = os.path.join(settings.MEDIA_ROOT, 'results/conversion', thumb_filename)
                    images[0].save(thumb_path, 'JPEG')
                    rel_thumb_path = os.path.relpath(thumb_path, settings.MEDIA_ROOT)
                    # Update status
                    task.status = 'done'
                    task.save()
                    download_url = settings.MEDIA_URL + rel_docx_path.replace('\\', '/')
                    thumbnail_url = settings.MEDIA_URL + rel_thumb_path.replace('\\', '/')
                    return JsonResponse({'success': True, 'task_id': task.id, 'download_url': download_url, 'thumbnail_url': thumbnail_url})
                except Exception as e:
                    print(traceback.format_exc())
                    return JsonResponse({'success': False, 'error': str(e)}, status=500)
            else:
                return JsonResponse({'success': False, 'error': 'Conversion type not implemented yet.'}, status=400)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

