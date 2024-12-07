import json
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

# Global variable to hold the model
model = None

# Load model once at the start
def load_model_once():
    global model
    try:
        model = load_model('app/models/Spiices.h5')  # Pastikan path sudah benar
        print("Model successfully loaded")
    except Exception as e:
        print(f"Error loading model: {e}")

# Load model and data on application startup
load_model_once()

def process_image(file):
    try:
        img = Image.open(file)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img = img.resize((224, 224))  # Sesuaikan dengan ukuran yang diharapkan model
        img_array = np.array(img)
        img_array = img_array / 255.0  # Normalisasi
        img_array = np.expand_dims(img_array, axis=0)  # Tambahkan batch dimension
        return img_array
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def validate_rempah(file):
    img_array = process_image(file)
    if img_array is None:
        return {"success": False, "message": "Invalid image or processing failed"}

    try:
        # Make sure model is loaded before prediction
        if model is None:
            return {"success": False, "message": "Model not loaded"}
        
        prediction = predict(model, img_array)
        
        if prediction["is_rempah"]:
            return {"success": True, "name": prediction["name"]}
        else:
            return {"success": False, "message": "Image is not a rempah"}
    except Exception as e:
        print(f"Error validating image: {e}")
        return {"success": False, "message": "Error during validation"}

def predict(model, img_array):
    try:
        # Melakukan prediksi menggunakan model
        predictions = model.predict(img_array)
        class_idx = np.argmax(predictions)  # Mendapatkan index kelas dengan probabilitas tertinggi
        
        # Class mapping, sesuaikan dengan label yang dimiliki model
        class_mapping = {
    0: "Adas", 1: "Andaliman", 2: "Asam Jawa", 3: "Bawang Bombai", 4: "Bawang Merah", 
    5: "Bawang Putih", 6: "Biji Ketumbar", 7: "Bukan Rempah", 8: "Bunga Lawang", 
    9: "Cengkeh", 10: "Daun Jeruk", 11: "Daun Kemangi", 12: "Daun Ketumbar", 
    13: "Daun Salam", 14: "Jahe", 15: "Jinten", 16: "Kapulaga", 17: "Kayu Manis", 
    18: "Kayu Secang", 19: "Kemiri", 20: "Kemukus", 21: "Kencur", 22: "Kluwek", 
    23: "Kunyit", 24: "Lada", 25: "Lengkuas", 26: "Pala", 27: "Saffron", 28: "Serai", 
    29: "Vanilli", 30: "Wijen"
}
        # Cek apakah hasil prediksi ada dalam class_mapping
        is_rempah = class_idx in class_mapping
        predicted_name = class_mapping.get(class_idx, "Unknown") if is_rempah else None
        
        # Jika bukan rempah, kembalikan is_rempah sebagai False dan pesan "Image is not a rempah"
        if not is_rempah:
            return {"is_rempah": False, "name": "Image is not a rempah"}
        
        return {"is_rempah": True, "name": predicted_name}
    except Exception as e:
        print(f"Error in prediction: {e}")
        return {"is_rempah": False, "name": "Unknown"}
