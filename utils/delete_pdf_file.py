from django.core.files.storage import default_storage

def delete_pdf_file(delete_pdf):
    if default_storage.exists(delete_pdf):
        default_storage.delete(delete_pdf)