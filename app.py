import os

from flask import Flask, render_template, request
import tools
from werkzeug.utils import secure_filename

app = Flask(__name__)


def create_image(image_path, button_value):
    new_image = tools.create_crossword_image(image_path, button_value)
    new_image.save(image_path)
    return image_path


@app.route('/', methods=['GET', 'POST'])
def index():
    result_image_path = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No image file provided'
        image_file = request.files['image']

        filename = secure_filename(image_file.filename)
        uploaded_image_path = os.path.join('static', 'images', filename)
        image_file.save(uploaded_image_path)

        button_value = request.form.get('button', '')
        if button_value != "Upload image":
            result_image_path = create_image(uploaded_image_path, button_value)

        uploaded_image_url = '\\' + uploaded_image_path
        return render_template('index.html', uploaded_image_url=uploaded_image_url, result_image_url=result_image_path,
                               button_value=button_value)
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
