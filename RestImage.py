from flask import Flask
from flask import request
import cv2
import Extraction as exctract

app = Flask(__name__)

@app.route('/image', methods=['POST'])
def get():
    img = request.files['image_data']
    image = cv2.imread(img.filename)
    plate = exctract.read(image)
    cv2.imwrite('output.png', image)
    return 'plate:'+plate

if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print(e)