from utils import generator


def new_input_pdf_path(input_pdf):
    new_input_pdf = str(input_pdf).replace("\\", "/")
    index = new_input_pdf.rfind("/")
    new_input_pdf = new_input_pdf[:index + 1] + f'{generator.random_generator()}.pdf'
    return new_input_pdf
