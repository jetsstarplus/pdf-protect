from django.http import JsonResponse
from flask import request
from itsdangerous import base64_encode
import PyPDF2
import base64
from rest_framework.decorators import api_view
import tempfile
import os;
  

# Create your views here.
@api_view(['GET', 'POST'])
def pdfprotect(request):
    b64file = bytes(request.data['attachment'],'utf-8')
    # b64file.decode('base64')
    password= request.data['password']
  
    pdf_in_file = tempfile.TemporaryFile()

    filedata=base64.decodebytes(b64file)
    pdf_in_file.write(filedata)
    
    inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
    pages_no = inputpdf.numPages
    output = PyPDF2.PdfFileWriter()

    for i in range(pages_no):
        output.addPage(inputpdf.getPage(i))

        output.encrypt(password)
        with open('outputPdf.pdf', 'wb') as outputStream:
            output.write(outputStream)
    with open('outputPdf.pdf', 'rb') as outputStream:
        encoded_string = base64.b64encode(outputStream.read())
    if os.path.exists("outputPdf.pdf"):
            os.remove('outputPdf.pdf')
    pdf_in_file.close()

    data = {'data':str(encoded_string.decode('utf-8'))}
    return JsonResponse(data)
