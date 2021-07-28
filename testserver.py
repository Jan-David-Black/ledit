import numpy as np
import cv2
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from PIL import Image

def erodeDialateAndSegment(gray, re, rd):
    thresh = cv2.threshold(gray, 0, 255,
	    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    element_erosion = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * re + 1, 2 * re + 1),
                                    (re, re))
    erosion_dst = cv2.erode(thresh, element_erosion)

    element_dialation = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * rd + 1, 2 * rd + 1),
                                    (rd, rd))
    dialation_dst = cv2.dilate(erosion_dst, element_dialation)
    
    output = cv2.connectedComponentsWithStats(
	    dialation_dst, True, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output
    
    output = labels.copy()*(255/np.max(labels))
    for i in range(1, numLabels):
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        (cX, cY) = centroids[i]

        cv2.rectangle(output, (x, y), (x + w, y + h), 100, 5)
        cv2.circle(output, (int(cX), int(cY)), 4, 200, -1)
    return (numLabels == 2),output


from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()

def from_base64(base64_data):
        nparr = np.fromstring(base64_data.decode('base64'), np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
        


def app(environ, start_response):
     # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except:
        request_body_size = 0

    if request_body_size == 0:
        status = '200 OK'
        response_headers = [
            ("Allow", "OPTIONS, POST"),
            ('Access-Control-Allow-Headers', '*'),
            ('Access-Control-Allow-Origin', '*')
        ]
        start_response(status, response_headers)
        return iter([])

    # When the method is POST the variable will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read(request_body_size)

    with open("tmp.png", 'wb') as image:
            image.write(base64.b64decode(request_body))

    image = cv2.imread("tmp.png", 0)

    image = cv2.pyrDown(image)
    image = cv2.pyrDown(image)
    

    plt.imsave("img.png", image)
    success, output = erodeDialateAndSegment(image, 2, 2)
    plt.imsave("out.png", output)

    """Simplest possible application object"""
    data = bytes(str(success), 'utf-8')
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data))),
        ('Access-Control-Allow-Origin', '*')
    ]
    start_response(status, response_headers)
    return iter([data])
