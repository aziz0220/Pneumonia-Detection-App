# app2.py
from flask import Flask, render_template, request, send_from_directory, url_for
import os
from test3 import get_prediction3
from test2 import get_prediction2
from test1 import get_prediction1
app = Flask(__name__)

# define the allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
wanteddirectory = '/home/aziz0220/mysite/uploads/'
# check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')


# add the serve_uploaded_file function
@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(wanteddirectory, filename)

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])

def predict():
    # Get the uploaded file from the request
    file = request.files['file']
    # Check if the file is allowed
    if not allowed_file(file.filename):
        return render_template('index.html', error1="Invalid file type. Please upload a file with a valid extension.")

    file.save(os.path.join(wanteddirectory, file.filename))
    # Get the selected model from the request
    selected_model = request.form['selected_model']
    # Call the appropriate prediction function based on the selected model
    if selected_model == 'model1':
        result, prediction0 = get_prediction1(file.filename, wanteddirectory)
    elif selected_model == 'model2':
        result, prediction0 = get_prediction2(file.filename, wanteddirectory)
    elif selected_model == 'model3':
        result, prediction0 = get_prediction3(file.filename, wanteddirectory)
    else:
        return render_template('index.html', error1="Invalid model selection.")

    # Add this to the predict() function
    image_path = os.path.join(wanteddirectory, file.filename)

   # Add this to the predict() function
    image_url = url_for('serve_uploaded_file', filename=file.filename)

    # Return the predicted result, percentage, and image URL
    return render_template('index.html', prediction1=result, percent=round(prediction0*100, 2), image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)

