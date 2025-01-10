from letter.models import Sender
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import io, os
from django.utils import timezone
from rest_framework import exceptions
from mtrk.settings import MEDIA_ROOT
from django.core.files.storage import default_storage
from utils.generator import code_generator
from utils.qrcode import create_qrcode
from authentication.models import User
from controller.models import Channel
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz
from utils.generator import code_generator, random_generator

def add_letter(data):
    code = code_generator()
    height = 550
    desc_height = 620
    start = 0
    end = 103
    line_spacing = 20 
    try:
        channel = Channel.objects.get(pk=data["channel_id"])
    except Channel.DoesNotExist:
        raise exceptions.ValidationError("Channel does not exist")

    # 3. PDF faylni yaratish
    buffer = io.BytesIO()  # PDF xotirada saqlanadi
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(375, 770, f"Televideniya va radio eshittirish")
    p.drawString(410, 750, f"arxiv fondi boshlig'i")
    p.drawString(412, 730, f"M.Utepbergenovga")
    p.setFont("Helvetica-Bold", 18)
    p.drawString(270, 650, f"BILDIRGI")
    p.setFont('DejaVuSans', size=10)
    # count = len(data["description"])
    # desc = "    " + data["description"]
    # p.drawString(80, 620, data["description"][:-8])
    # p.drawString(60, 600, data["description"][:-4])
    # p.drawString(60, 580, data["description"][:-4])

    desc_count = len(data["description"])
    desc = "    " + data["description"]
    while desc_count > 0:
        p.drawString(60, desc_height, desc[start: end])
        desc_height -= 20
        desc_count -= 103
        start += 103
        end += 103

    p.setFont('DejaVuSans', size=10)
    for item in data['bookmarks']:
        id_str = str(item['id'])
        title_str = str(item['title'])
        p.drawString(120, height, id_str)
        p.drawString(150, height, title_str)
        height -= line_spacing
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, 90, f'"{channel.name}" telekanali')
    p.drawString(412, 90, f'"{channel.director.full_name}"')
    
    # 5. PDFni saqlash
    p.showPage()
    p.save()

    buffer.seek(0)  # Fayl boshiga qaytarish
    pdf_content = ContentFile(buffer.read(), f"{code}.pdf")
    print(pdf_content)
    return pdf_content


# @shared_task
def edit_channel_derictor(input_pdf, username, pk):
    # notice = Notice.objects.get(pk=pk)
    # 1. QR-kodni yaratish
    input_pdf = MEDIA_ROOT / input_pdf
    qr_data = f"Foydalanuvchi: {username}\nVaqt: {timezone.now().strftime('%d.%m.%Y %H:%M:%S')}"
    pdf_document = fitz.open(input_pdf)
    
    # QR-kodni yaratish
    qr_code_image = create_qrcode(qr_data)

    # Har bir sahifani tahrirlash
    for page in pdf_document:
        # QR-kodni sahifaga joylashtirish
        rect = fitz.Rect(370, 700, 450, 780)  # QR-kod uchun joy (x1, y1, x2, y2)
        page.insert_image(rect, stream=qr_code_image)
    lst = str(input_pdf).split("\\")
    lst[len(lst)-1] = f'{random_generator()}.pdf'
    output_pdf = ''
    for item in lst:
        output_pdf += item + '/'
    # Yangi PDFni saqlash
    # a = input_pdf
    # os.remove(input_pdf)
    print(output_pdf)
    pdf_document.save(output_pdf[:-1])
    path = output_pdf.split('/media/')[-1][:-1]
    # notice.file = path
    # notice.save()
    if default_storage.exists(input_pdf):
        default_storage.delete(input_pdf)
    

# @shared_task
def edit_archive_derictor(input_pdf, username, pk):
    # notice = Notice.objects.get(pk=pk)
    # 1. QR-kodni yaratish
    input_pdf = MEDIA_ROOT / input_pdf
    qr_data = f"Foydalanuvchi: {username}\nVaqt: {timezone.now().strftime('%d.%m.%Y %H:%M:%S')}"
    pdf_document = fitz.open(input_pdf)
    
    # QR-kodni yaratish
    qr_code_image = create_qrcode(qr_data)

    # Har bir sahifani tahrirlash
    for page in pdf_document:
        # QR-kodni sahifaga joylashtirish
        rect = fitz.Rect(70, 60, 140, 130)  # QR-kod uchun joy (x1, y1, x2, y2)
        page.insert_image(rect, stream=qr_code_image)
    lst = str(input_pdf).split("\\")
    lst[len(lst)-1] = f'{random_generator()}.pdf'
    output_pdf = ''
    for item in lst:
        output_pdf += item + '/'
    # Yangi PDFni saqlash
    pdf_document.save(output_pdf[:-1])
    path = output_pdf.split('/media/')[-1][:-1]
    # notice.file = path
    # notice.save()
