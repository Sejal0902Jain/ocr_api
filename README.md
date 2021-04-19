## Requirements:
Download and install tesseract.exe

Download and install poppler

## Run:
pip install -r requirements.txt

python app.py

### Docker-compose way
* To start app, run command `docker-compose up --build`
* To stop app, run command `Ctrl+C` and then `docker-compose down`

## API LINK to be used: 
http://127.0.0.1:5000/convert

## JSON body to be posted: 
{ "path_PDF" : "Blood Report 1.pdf" }
