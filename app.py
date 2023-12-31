import os
import time
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from pytorch_tabnet.tab_model import TabNetClassifier

# Load the TabNet model from Module 5
model_path = './data_tabular.zip'  
class_list = {
    'Pemasukan kurang dari 50k': 0,
    'Pemasukan lebih dari 50k': 1
}

# Create a Flask web application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('awalan.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    return render_template('index.html')

# Define a route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Coba untuk memuat model
            loaded_model = TabNetClassifier()
            loaded_model.load_model(model_path)
        except FileNotFoundError:
            # Tangani kesalahan jika file tidak ditemukan
            return render_template('error.html', message="Model file not found.")

        # Dapatkan data input dari form
        age = float(request.form['age'])
        edu = float(request.form['education'])
        ocu = float(request.form['occupation'])
        hours = float(request.form['hours_per_week'])
        start = time.time()
        # Lakukan prediksi menggunakan model yang dimuat
        probabilities = loaded_model.predict(np.array([[age, edu, ocu, hours]]))
        runtimes = round(time.time() - start, 4)
        # Konversi list ke string sebelum mengembalikannya
        result = probabilities.tolist()[0]
        prediction_label = list(class_list.keys())[result]

        # Tampilkan prediksi di halaman hasil
        return render_template('/predict.html', prediction=prediction_label, runtime=runtimes)

if __name__ == '__main__':
    # Jalankan aplikasinya
    app.run(debug=True)