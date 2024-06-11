import os
import sys
import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Lấy đường dẫn của thư mục hiện tại
current_dir = os.getcwd()
sys.stdout.reconfigure(encoding='utf-8')

# Đường dẫn đến các file cần thiết
tokenizer_path = os.path.join(current_dir, "tokenizer.pickle")
label_dict_path = os.path.join(current_dir, "label_dict.pickle")
model_path = os.path.join(current_dir, "math_problem_model.h5")

# Load các thành phần cần thiết từ các file
with open(tokenizer_path, "rb") as f:
    tokenizer = pickle.load(f)

with open(label_dict_path, "rb") as f:
    label_dict = pickle.load(f)

model = load_model(model_path)

# Định nghĩa max_len (độ dài tối đa của sequence)
max_len = 244  # Giá trị này phải tương ứng với giá trị sử dụng khi train model

# Biến toàn cục để lưu trạng thái người dùng
user_state = {
    "mode": "normal"  # Các giá trị có thể là "normal", "awaiting_exercises"
}

@app.route('/')
def index():
    return "Xin chào, đây là điểm cuối gốc. Hãy thử gửi một yêu cầu POST đến /api."

@app.route('/api', methods=['POST'])
def respond():
    data = request.get_json()
    message = data.get('message').lower()

    if user_state["mode"] == "awaiting_exercises":
        # Chuyển nội dung bài tập đến hàm dự đoán
        prediction_result = predict_problem(message)
        # Trả về kết quả dự đoán
        response_message = f"Kết quả dự đoán: {prediction_result['predicted_label']}"
        return jsonify({"message": response_message})

    # Basic communication phrases in Vietnamese
    basic_phrases = {
        "xin chào": "Chào bạn! Tôi có thể giúp gì cho bạn?",
        "chào": "Xin chào! Tôi có thể hỗ trợ gì cho bạn?",
    }

    # Customer service related responses for chatbot business
    customer_service_phrases = {
        "bạn có thể làm gì": "Bạn có thể bắt đầu bằng cách đăng ký trên trang web của chúng tôi và làm theo hướng dẫn để cấu hình chatbot.",
        "tạo bài tập": "Hãy nhập bài tập vào khung chat, tôi sẽ tạo ra thêm cho bạn."
    }

    # Combine both dictionaries
    all_phrases = {**basic_phrases, **customer_service_phrases}
    
    # Find response based on message
    response_message = all_phrases.get(message, f"Bạn đã nói: {message}")

    if message == "tạo bài tập":
        response_message += " Bây giờ hãy gửi bài tập của bạn để tôi nhận diện."
        user_state["mode"] = "awaiting_exercises"

    return jsonify({"message": response_message})

def predict_problem(problem):
    sequences = tokenizer.texts_to_sequences([problem])
    X = pad_sequences(sequences, maxlen=max_len)
    predictions_proba = model.predict(X)
    predicted_label = np.argmax(predictions_proba, axis=1)[0]
    predicted_label_name = [name for name, label in label_dict.items() if label == predicted_label][0]
    return {"problem": problem, "predicted_label": predicted_label_name}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
