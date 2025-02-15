from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# 1. Configure where files get uploaded
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    # This will just render a basic upload form (we'll create upload.html next)
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has a file part
    if 'file' not in request.files:
        return "No file part in the request."
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submits an empty part without filename
    if file.filename == '':
        return "No selected file."

    # Save file to the uploads folder
    if file:
        # Secure the filename, but for simplicity, we’ll just use file.filename.
        # In production, consider using secure_filename from Werkzeug.
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Redirect or render a template to show success
        return redirect(url_for('success', filename=filename))

@app.route('/success/<filename>')
def success(filename):
    return f"File '{filename}' uploaded successfully!"

if __name__ == '__main__':
    # Create 'uploads' folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)
