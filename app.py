from flask import Flask, request, send_file, render_template
import qrcode
from io import BytesIO
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form['data']

    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convertir la imagen a bytes
    img_bytes = BytesIO()
    img.save(img_bytes)
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

if __name__ == '__main__':
    freezer.freeze()
    app.run(debug=True)
