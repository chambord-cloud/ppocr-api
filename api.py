from flask import Flask, request, jsonify, Response
from gevent import pywsgi
import json
import base64
import paddleocr
import io
from PIL import Image
import numpy
from http import HTTPStatus

app = Flask(__name__)


@app.route('/api/ocr', methods=["POST"])
def ocr():
    try:
        data = request.get_json()
        if (request.data == ''):
            print("empty data")
            return Response(status=HTTPStatus.NO_CONTENT)
        imageData = data["image"]
        imgBytes = base64.b64decode(imageData)
        image = io.BytesIO(imgBytes)
        tmpFile = Image.open(image)
        img = numpy.array(tmpFile)[:, :, :3]
        result = ppocr.ocr(img, cls=True)
        return jsonify(result)
    except:
        return Response(status=HTTPStatus.BAD_REQUEST)


def main():
    global ppocr
    ppocr = paddleocr.PaddleOCR(use_angle_cls=True, use_gpu=False)
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()


if __name__ == "__main__":
    main()
