# import the necessary packages
from flask import Flask, request, Response
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os


def process(pdf):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  
    # path of tesseract.exe 
    PDF_file = pdf
    pages = convert_from_path(PDF_file, 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')  
    # poppler_path 
    # print(pdf)

    image_counter = 1
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1
    
    filelimit = image_counter-1
    outfile = "output.txt"
    
    f = open(outfile, "a")
    for i in range(1, filelimit + 1):
        filename = "page_"+str(i)+".jpg"
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        os.remove(filename)
        text = text.replace('-\n', '')    
        f.write(text)
    
    f.close()
    return f


PROJECT_HOME = os.path.dirname(os.path.realpath(".\\api_ocrpdf"))
UPLOAD_FOLDER  = '{}\\api_ocrpdf'.format(PROJECT_HOME)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  

@app.route("/", methods=['GET','POST'])
def upload():
    return "OCR_PDF"

@app.route('/convert', methods = ['POST'])  
def convert():  
    if request.method == 'POST':
        request_data = request.get_json()
        name= str(request_data['path_PDF'])

    if not os.path.exists(name):
        status_code = Response(status=404)
        return status_code

    # Check if path is a file and serve
    else:
        fil = process(name)
        status_code = Response(status=200)
        return status_code

if __name__ == "__main__":
    app.debug = False
    app.run()
