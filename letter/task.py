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
from authentication.models import User
from controller.models import Channel
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/DejaVuSans.ttf'))

def add_letter(data, info_data):
    code = code_generator()
    height = 550
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
    p.drawString(80, 620, data["description"][:-8])
    p.drawString(60, 600, data["description"][:-4])
    p.drawString(60, 580, data["description"][:-4])

    p.setFont('DejaVuSans', size=10)
    for item in info_data:
        i = str(item['i']) + '.'
        id_str = str(item['id'])
        title_str = str(item['title'])
        p.drawString(80, height, i)
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
    return (pdf_content, channel.director)


# @shared_task
# def edit_channel_derictor(input_pdf, username, pk):
#     notice = Notice.objects.get(pk=pk)
#     # 1. QR-kodni yaratish
#     input_pdf = MEDIA_ROOT / input_pdf
#     qr_data = f"Foydalanuvchi: {username}\nVaqt: {timezone.now().strftime('%d.%m.%Y %H:%M:%S')}"
#     pdf_document = fitz.open(input_pdf)
    
#     # QR-kodni yaratish
#     qr_code_image = create_qrcode(qr_data)

#     # Har bir sahifani tahrirlash
#     for page in pdf_document:
#         # Matnni sahifaga qo'shish
#         page.insert_text((90, 730), "direktori", fontsize=12, color=(0, 0, 0))  # (x, y) koordinatalar
#         page.insert_text((460, 740), username, fontsize=12, color=(0, 0, 0))  # (x, y) koordinatalar
#         # QR-kodni sahifaga joylashtirish
#         rect = fitz.Rect(370, 700, 450, 780)  # QR-kod uchun joy (x1, y1, x2, y2)
#         page.insert_image(rect, stream=qr_code_image)
#     lst = str(input_pdf).split("\\")
#     lst[len(lst)-1] = '222222222222222222.pdf'
#     output_pdf = ''
#     for item in lst:
#         output_pdf += item + '/'
#     # Yangi PDFni saqlash
#     # a = input_pdf
#     # os.remove(input_pdf)
#     print(output_pdf)
#     pdf_document.save(output_pdf[:-1])
#     path = output_pdf.split('/media/')[-1][:-1]
#     notice.file = path
#     notice.save()
#     if default_storage.exists(input_pdf):
#         default_storage.delete(input_pdf)
    

# @shared_task
# def edit_archive_derictor(input_pdf, username, pk):
#     notice = Notice.objects.get(pk=pk)
#     # 1. QR-kodni yaratish
#     input_pdf = MEDIA_ROOT / input_pdf
#     qr_data = f"Foydalanuvchi: {username}\nVaqt: {timezone.now().strftime('%d.%m.%Y %H:%M:%S')}"
#     pdf_document = fitz.open(input_pdf)
    
#     # QR-kodni yaratish
#     qr_code_image = create_qrcode(qr_data)

#     # Har bir sahifani tahrirlash
#     for page in pdf_document:
#         # QR-kodni sahifaga joylashtirish
#         rect = fitz.Rect(70, 60, 140, 130)  # QR-kod uchun joy (x1, y1, x2, y2)
#         page.insert_image(rect, stream=qr_code_image)
#     lst = str(input_pdf).split("\\")
#     lst[len(lst)-1] = '333333333333333333333.pdf'
#     output_pdf = ''
#     for item in lst:
#         output_pdf += item + '/'
#     # Yangi PDFni saqlash
#     pdf_document.save(output_pdf[:-1])
#     path = output_pdf.split('/media/')[-1][:-1]
#     notice.file = path
#     notice.save()
