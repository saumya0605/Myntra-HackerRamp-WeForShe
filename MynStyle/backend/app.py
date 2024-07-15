from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
import numpy as np
import pandas as pd
import pickle
from io import BytesIO
import base64
from PIL import Image
from sklearn.neighbors import NearestNeighbors
from numpy.linalg import norm
import tensorflow
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import gzip
import os
import requests
# Initialize Flask application
application = Flask(__name__)
CORS(application, origins='*')  # Allow CORS for all origins

# Load Myntra Dataset and other initialization code...

# Load the Myntra dataset
myntra = pd.read_csv('myntra.csv')

# Load the similarity arrays using gzip
with gzip.open('sig1.npy.gz', 'rb') as f:
    sig1 = np.load(f)

with gzip.open('sig2.npy.gz', 'rb') as f:
    sig2 = np.load(f)

with gzip.open('sig3.npy.gz', 'rb') as f:
    sig3 = np.load(f)

with gzip.open('sig4.npy.gz', 'rb') as f:
    sig4 = np.load(f)

# Merge arrays vertically
sig = np.vstack((sig1, sig2, sig3, sig4))

# Load indices for product titles
indices = pickle.load(open('indices.pkl', 'rb'))

# Load embeddings
embeddings = np.array(pickle.load(open('embeddings.pkl', 'rb')))

# Load popular products for men and women
men_popular = pd.read_pickle(r'men_popular.pkl')
women_popular = pd.read_pickle(r'women_popular.pkl')
popular_products = pd.read_pickle(r'popular_products.pkl')

# Load filtered indices
filtered_indices = np.array(pd.read_pickle(r'filtered_indices.pkl'))

# Initialize ResNet model
model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model.trainable = False

model = tensorflow.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])

# Function to extract features from image
def feature_extraction(img_array, model):
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(expanded_img_array).flatten()
    return result / norm(result)

# Function to recommend similar products
def recommend(features, feature_list):
    neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
    neighbors.fit(feature_list)
    distances, indices = neighbors.kneighbors([features])
    return indices

# Routes with CORS enabled

@application.route('/bestsellers', methods=['GET'])
def get_data():
    return popular_products.to_json(orient='records')

@application.route('/menProducts', methods=['GET'])
def get_men_data():
    return men_popular.to_json(orient='records')

@application.route('/womenProducts', methods=['GET'])
def get_women_data():
    return women_popular.to_json(orient='records')

@application.route('/allProducts', methods=['GET'])
def get_all_data():
    return myntra.to_json(orient='records')

@application.route('/prod/<title>', methods=['GET'])
def get_prod(title):
    index = indices[title]
    sig_cs = list(enumerate(sig[index]))
    sig2 = sorted(sig_cs, key=lambda x: x[1], reverse=True)
    sig_cs2 = sig2[1: 13]
    product_indices = [i[0] for i in sig_cs2]
    return myntra.iloc[product_indices].to_json(orient='records')

@application.route('/recommand/<title>', methods=['GET'])
def get_recommand(title):
    index = np.where(myntra['title'] == title)[0][0]
    output = filtered_indices[index][1:]
    return myntra.iloc[output].to_json(orient='records')

@application.route('/imageData', methods=['POST'])
def get_image_data():
    img_data = request.get_json()
    img = img_data['data'][23:]
    im = Image.open(BytesIO(base64.b64decode(img))).resize((224, 224))
    img_array = np.array(im)
    features = feature_extraction(img_array, model)
    indices = recommend(features, embeddings)
    return myntra.iloc[indices[0]].to_json(orient='records')

@application.route('/tryall', methods=['POST'])
def tryall():
    try:
        # Extract image URLs from the request (assuming comma-separated URLs)
        image_urls = request.form['mydata'].split(',')
        
        # Create a folder if it doesn't exist
        downloads_folder = 'downloads'
        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder)
        
        image_paths = []
        for idx, url in enumerate(image_urls):
            response = requests.get(url)
            if response.status_code == 200:
                filename = os.path.join(downloads_folder, f'image_{idx}.png')  # Generate a unique filename in the downloads folder
                with open(filename, 'wb') as f:
                    f.write(response.content)
                image_paths.append(filename)
        
        # Run your CV loop with downloaded image paths
        os.system('python test.py ' + ' '.join(image_paths))
        
        return jsonify({'status': 'success'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
if __name__ == '__main__':
    application.run()
