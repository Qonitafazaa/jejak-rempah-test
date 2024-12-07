from tensorflow.keras.models import load_model
import numpy as np

model = load_model('models/Spiices.h5')

def predict_rempah(image_data):
    prediction = model.predict(image_data)  # Prediksi menggunakan model
    # Misalnya model mengeluarkan probabilitas untuk tiap kelas, kita ambil yang tertinggi
    predicted_class = np.argmax(prediction)
    return predicted_class  # Kelas prediksi
