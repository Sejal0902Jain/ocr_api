# import the necessary packages
import os
from flask import Flask, request, render_template
from imutils import paths
import cv2
import pytesseract
import numpy as np
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os


def convert(pdf):
    PDF_file = pdf
    pages = convert_from_path(PDF_file, 500,poppler_path=r'C:\Users\DELL\poppler-0.68.0_x86\poppler-0.68.0\bin')   

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



#specify the default folder from where the files will be selected and uploaded
PROJECT_HOME = os.path.dirname(os.path.realpath("C:\\Users\\DELL\\Desktop\\UK\\wetransfer-9d5256\\api_ocrpdf"))
UPLOAD_FOLDER  = '{}\\api_ocrpdf'.format(PROJECT_HOME)

#folder uploaded
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  

#to access that particular folder to upload the files and display it in this format
@app.route("/", methods=['GET','POST'])
def upload():
    # return render_template('upload.html')
    return """
        <!doctype html>
        <title>Upload pdf for OCR</title>
        <h1>Upload pdf for OCR</h1>
        <form action="/success" method="post" enctype="multipart/form-data">
          <p><input type="file" name="file"/>
             <input type="submit" value="Upload">
        </form>
        """

#main logic to process the OCR on the uploaded file and display it on the local website by rendering the html template
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)  
        name=f.filename
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'    
    print(f,name)
    PDF_file = f
    fil = convert(name)
    with open(fil.name, 'r') as f: 
        return render_template('content.html', text=f.read()) 

if __name__ == "__main__":
    app.debug = False
    app.run()
