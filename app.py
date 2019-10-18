import os
import requests
from flask import Flask
from flask import render_template

# File upload APIs
from flask import flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# region declare file upload particulars
if os.path.exists('./uploads'):
    print('Upload folder exists')
else:
    os.mkdir('./uploads')
    print('Made upload dir')

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'gif', 'png', 'jpg', 'jpeg', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# function to verify if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# endregion

# region define the classifier resource
@app.route('/classify-image/<filename>')
def classify_image(filename):

    media_type = 'image'
    media_url = os.path.join('/', app.config['UPLOAD_FOLDER'], filename)

    return render_template('classification_result.html',
                           media_type=media_type,
                           media_url=media_url,
                           class_name='monkey',
                           classification_result_info='some dict')
# endregion

# region define root resource - which is a file upload resource
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser can also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # valid case
        if file and allowed_file(file.filename):
            # print('valid post case')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))

            return redirect(url_for('classify_image',
                                    filename=filename))

    # Case if method is GET - return HTML page
    # print('get case')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
# endregion

# region define file download resource - deprecated
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
# endregion

if __name__ == '__main__':
    app.run()