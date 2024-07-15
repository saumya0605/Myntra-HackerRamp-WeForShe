from flask import Flask, render_template, Response, redirect, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
import bson
from bson.objectid import ObjectId
from camera import VideoCamera

app = Flask(__name__)
CORS(app)

CART = []
app.config["MONGO_URI"] = "mongodb+srv://admindb:admindatabase@cluster0-vlwic.mongodb.net/myntra"
mongo = PyMongo(app)
db_operations = mongo.db.products

@app.route('/tryon/<file_path>', methods=['POST', 'GET'])
def tryon(file_path):
    file_path = file_path.replace(',', '/')
    os.system('python tryOn.py ' + file_path)
    return redirect('http://127.0.0.1:5000/', code=302, Response=None)

@app.route('/tryall', methods=['POST', 'GET'])
def tryall():
    CART = request.form['mydata'].replace(',', '/')
    os.system('python test.py ' + CART)
    return render_template('checkout.html', message='')

@app.route('/')
def indexx():
    return render_template('home.html')

@app.route('/read')
def read():
    users = db_operations.find()
    output = [{'Label': user['Label']} for user in users]
    return jsonify(output)

@app.route('/product')
def product():
    return render_template('product.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/cart/<file_path>", methods=['POST', 'GET'])
def cart(file_path):
    global CART
    file_path = file_path.replace(',', '/')
    print("ADDED", file_path)
    CART.append(file_path)
    return render_template("checkout.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()


    #dataToSend static/images/Tops4/15.png