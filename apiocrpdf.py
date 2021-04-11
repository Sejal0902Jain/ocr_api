# import the necessary packages
from flask import Flask, request, render_template
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os


def convert(pdf):
    PDF_file = pdf
    pages = convert_from_path(PDF_file, 500,poppler_path=r'C:\Users\DELL\poppler-0.68.0_x86\poppler-0.68.0\bin')  
    # poppler_path 

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
    return """
        <!doctype html>
        <title>Upload pdf for OCR</title>
        <h1>Upload pdf for OCR</h1>
        <form action="/success" method="post" enctype="multipart/form-data">
          <p><input type="file" name="file"/>
             <input type="submit" value="Upload">
        </form>
        """

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)  
        name=f.filename
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  
    # path of tesseract.exe 
    print(f,name)
    PDF_file = f
    fil = convert(name)
    with open(fil.name, 'r') as f: 
        return render_template('content.html', text=f.read()) 

if __name__ == "__main__":
    app.debug = False
    app.run()
