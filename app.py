from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from azure.storage.blob import BlockBlobService, PublicAccess
import rsa
from cryptography.fernet import Fernet
import os
import string
import random
import requests

app = Flask(__name__)
account = 'YOUR ACCOUNT NAME'
container = 'YOUR CONATAINER NAME'
key = 'YOUR KEY'

key = Fernet.generate_key()
print(key)
fernet = Fernet(key)


blob_service = BlockBlobService(
    account_name=account, account_key=key)


@app.route('/')
def home():
   return render_template('home.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      filename = secure_filename(file.filename)
      encfile = fernet.encrypt(filename.encode())
       
   try:
            blob_service.create_blob_from_stream(container,encfile ,file)
   except Exception:
            print (Exception) 
            pass
   
   return render_template('success.html')
   return '''
      <!doctype html>
      <title>Upload new File</title>
      <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
