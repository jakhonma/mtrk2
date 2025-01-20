from mtrk.settings import MEDIA_ROOT
from utils.qrcode import create_qrcode
import fitz
from utils import choices, time_tashkent_now, doc_path


def qrcode_data(letter, user, now):
    body = f"\nFoydalanuvchi: {user.full_name}\nVaqt: {now.strftime('%d.%m.%Y %H:%M:%S')}"
    if user.role == choices.UserRole.ARCHIVE_DIRECTOR:
        qr_data = f"Media Fond" + body
    else:
        qr_data = f"Kanal: {letter.channel.name}" + body
    return qr_data


def new_pdf_doc(letter, user, x, y):
    input_pdf = MEDIA_ROOT / letter.pdf.name

    now = time_tashkent_now.current_time_tashkent_now(letter)
    pdf_document = fitz.open(input_pdf)

    qr_data = qrcode_data(letter, user, now)
    qr_code_image = create_qrcode(qr_data)

    first_page = pdf_document[0]
    rect = fitz.Rect(x, y, x + 45, y + 45)
    first_page.insert_image(rect, stream=qr_code_image)

    # for page in pdf_document:
    #     rect = fitz.Rect(x, y, x + 50, y + 50)
    #     page.insert_image(rect, stream=qr_code_image)

    new_input_pdf = doc_path.new_input_pdf_path(input_pdf=input_pdf)
    pdf_document.save(new_input_pdf)
    path = new_input_pdf.split('/media/')[-1]
    # letter.pdf = path
    # letter.save()
    return path, input_pdf


def edit_channel_director(letter, user):
    return new_pdf_doc(letter=letter, user=user, x=295, y=755)


# @shared_task
def edit_archive_director(letter, user):
    return new_pdf_doc(letter=letter, user=user, x=75, y=65)
