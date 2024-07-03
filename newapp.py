import json
import numpy as np
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModel
from flask import Flask, request, jsonify
from flask_cors import CORS
from underthesea import word_tokenize
import re
import os
import faiss
import pandas as pd
from tensorflow.keras.optimizers import Adam # type: ignore
from tensorflow.keras.regularizers import l2 # type: ignore
# from google.cloud import vision
import io
import os
import base64
import sys
# from model.ocr_module import detect_text
from topics.topics import topics
from bai_tap.bien_doi_deu_van_dung import  generate_problem_and_solution
from bai_tap.thang_deu_van_dung import generate_problem_and_solution_2
from bai_tap.roi_tu_do_van_dung import generate_problem_and_solution_3
from bai_tap.thang_deu_van_dung_cao import generate_problem_and_solution_5
from bai_tap.bien_doi_deu_van_dung_cao import generate_problem_and_solution_6
from bai_tap.nem_xien_van_dung import generate_problem_and_solution_7

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


class PhoBERTLayer(tf.keras.layers.Layer):
    def __init__(self, phobert_model_name="vinai/phobert-base", **kwargs):
        super(PhoBERTLayer, self).__init__(**kwargs)
        self.phobert_model_name = phobert_model_name
        self.phobert_model = TFAutoModel.from_pretrained(phobert_model_name)

    def call(self, inputs):
        input_ids, attention_mask = inputs
        outputs = self.phobert_model(input_ids=input_ids, attention_mask=attention_mask)
        return outputs.last_hidden_state

    def get_config(self):
        config = super(PhoBERTLayer, self).get_config()
        config.update({"phobert_model_name": self.phobert_model_name})
        return config

    @classmethod
    def from_config(cls, config):
        phobert_model_name = config.pop("phobert_model_name", "vinai/phobert-base")
        config.pop("phobert_model", None)
        return cls(phobert_model_name=phobert_model_name, **config)

# Initialize and load PhoBERT model before using the custom layer
phobert_model_name = "vinai/phobert-base"
phobert_model = TFAutoModel.from_pretrained(phobert_model_name)
tokenizer = AutoTokenizer.from_pretrained(phobert_model_name)

# Define custom objects
custom_objects = {"PhoBERTLayer": PhoBERTLayer}

# Load the model
model = tf.keras.models.load_model('model/physics_model.keras', custom_objects=custom_objects)

# Load the label dictionary
with open('model/physics_label_dict.json', 'r') as f:
    label_dict = json.load(f)

# Set max length for input sequences
max_len = 128

def encode_texts(texts, tokenizer, max_len):
    encodings = tokenizer(texts, truncation=True, padding='max_length', max_length=max_len, return_tensors='tf')
    return encodings['input_ids'], encodings['attention_mask']

uniform_keywords = ["vận tốc không đổi", "chuyển động thẳng đều", "tốc độ trung bình", "tốc độ không đổi", "chuyển động đều", "không thay đổi tốc độ"]
accelerated_keywords = ["gia tốc", "vận tốc thay đổi", "tăng tốc", "biến đổi", "chậm dần đều", "nhanh dần đều", "gia tốc không đổi", "vận tốc ban đầu", "vận tốc cuối", "thời gian đạt được vận tốc", "hãm phanh"]

def keyword_features(text, uniform_keywords, accelerated_keywords):
    uniform_count = sum([keyword in text for keyword in uniform_keywords])
    accelerated_count = sum([keyword in text for keyword in accelerated_keywords])
    return uniform_count, accelerated_count

def adjust_probabilities(text, probabilities, uniform_keywords, accelerated_keywords):
    uniform_count, accelerated_count = keyword_features(text, uniform_keywords, accelerated_keywords)
    adjustment_factor = 2

    uniform_label_index = label_dict.get('chuyển động thẳng đều')
    accelerated_label_index = label_dict.get('chuyển động thẳng biến đổi đều')

    if uniform_count > 0 and uniform_label_index is not None:
        probabilities[uniform_label_index] *= adjustment_factor
    if accelerated_count > 0 and accelerated_label_index is not None:
        probabilities[accelerated_label_index] *= adjustment_factor

    probabilities /= probabilities.sum()
    return probabilities


def remove_html(txt):
    return re.sub(r'<[^>]*>', '', txt)

def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split('|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split('|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic

dicchar = loaddicchar()

def convert_unicode(txt):
    return re.sub('|'.join(dicchar.keys()), lambda x: dicchar[x.group()], txt)

def chuan_hoa_dau_tu_tieng_viet(word):
    bang_nguyen_am = [
        ["a", "à", "á", "ả", "ã", "ạ"],
        ["ă", "ằ", "ắ", "ẳ", "ẵ", "ặ"],
        ["â", "ầ", "ấ", "ẩ", "ẫ", "ậ"],
        ["e", "è", "é", "ẻ", "ẽ", "ẹ"],
        ["ê", "ề", "ế", "ể", "ễ", "ệ"],
        ["i", "ì", "í", "ỉ", "ĩ", "ị"],
        ["o", "ò", "ó", "ỏ", "õ", "ọ"],
        ["ô", "ồ", "ố", "ổ", "ỗ", "ộ"],
        ["ơ", "ờ", "ớ", "ở", "ỡ", "ợ"],
        ["u", "ù", "ú", "ủ", "ũ", "ụ"],
        ["ư", "ừ", "ứ", "ử", "ữ", "ự"],
        ["y", "ỳ", "ý", "ỷ", "ỹ", "ỵ"]
    ]
    nguyen_am_to_ids = {}
    for i in range(len(bang_nguyen_am)):
        for j in range(len(bang_nguyen_am[i])):
            nguyen_am_to_ids[bang_nguyen_am[i][j]] = (i, j)

    dau_cau = 0
    nguyen_am_index = []
    qu_or_gi = False
    chars = list(word)
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x == -1:
            continue
        if x == 9:
            if index != 0 and chars[index - 1] == 'q':
                chars[index] = 'u'
                qu_or_gi = True
        elif x == 5:
            if index != 0 and chars[index - 1] == 'g':
                chars[index] = 'i'
                qu_or_gi = True
        if y != 0:
            dau_cau = y
            chars[index] = bang_nguyen_am[x][0]
        if not qu_or_gi or index != 1:
            nguyen_am_index.append(index)

    if not nguyen_am_index:
        return word

    if len(nguyen_am_index) < 2:
        if qu_or_gi:
            if len(chars) == 2:
                x, y = nguyen_am_to_ids.get(chars[1])
                chars[1] = bang_nguyen_am[x][dau_cau]
            else:
                x, y = nguyen_am_to_ids.get(chars[2], (-1, -1))
                if x != -1:
                    chars[2] = bang_nguyen_am[x][dau_cau]
                else:
                    chars[1] = bang_nguyen_am[5][dau_cau] if chars[1] == 'i' else bang_nguyen_am[9][dau_cau]
        else:
            x, y = nguyen_am_to_ids.get(chars[nguyen_am_index[0]])
            chars[nguyen_am_index[0]] = bang_nguyen_am[x][dau_cau]
    else:
        if len(nguyen_am_index) == 2 and nguyen_am_index[-1] == len(chars) - 1:
            x, y = nguyen_am_to_ids.get(chars[nguyen_am_index[0]])
            chars[nguyen_am_index[0]] = bang_nguyen_am[x][dau_cau]
        else:
            x, y = nguyen_am_to_ids.get(chars[nguyen_am_index[1]])
            chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    return ''.join(chars)

def chuan_hoa_dau_cau_tieng_viet(sentence):
    words = sentence.split()
    for index, word in enumerate(words):
        prefix = re.match(r'^\W+', word)
        suffix = re.match(r'\W+$', word)
        prefix = prefix.group() if prefix else ''
        suffix = suffix.group() if suffix else ''
        cw = re.sub(r'^\W+|\W+$', '', word)
        if len(cw) == 0:
            continue
        cw = chuan_hoa_dau_tu_tieng_viet(cw)
        words[index] = prefix + cw + suffix
    return ' '.join(words)

def remove_punctuation(txt):
    return re.sub(r'[^\w\s]', '', txt)

def chuan_hoa_khoang_trang(txt):
    return re.sub(r'\s+', ' ', txt).strip()

def tokenize(txt):
    return ' '.join(word_tokenize(txt))

def clean_text(text):
    text = remove_html(text)
    text = convert_unicode(text)
    text = chuan_hoa_dau_cau_tieng_viet(text)
    text = text.lower()
    text = remove_punctuation(text)
    text = chuan_hoa_khoang_trang(text)
    text = tokenize(text)
    return text


# def detect_text(image_content, credentials_path):
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
#     client = vision.ImageAnnotatorClient()
#     image = vision.Image(content=image_content)
#     response = client.text_detection(image=image)
#     texts = response.text_annotations

#     if texts:
#         full_text = texts[0].description
#         return full_text
#     else:
#         return None



class Retriever:
    def __init__(self, knowledge_base_path, tokenizer, phobert_model):
        self.knowledge_base = pd.read_csv(knowledge_base_path)  # Đọc từ file CSV
        self.tokenizer = tokenizer
        self.phobert_model = phobert_model
        self.index = faiss.IndexFlatL2(768)
        self.build_index()

    def build_index(self):
        embeddings = []
        for problem in self.knowledge_base['problem']:
            input_ids = self.tokenizer(problem, return_tensors='tf', padding=True, truncation=True, max_length=128)['input_ids']
            embedding = self.phobert_model(input_ids)[0]
            embedding = tf.reduce_mean(embedding, axis=1).numpy()
            embeddings.append(embedding)
        embeddings = np.vstack(embeddings)
        self.index.add(embeddings)

    def retrieve(self, query, top_k=5):
        input_ids = self.tokenizer(query, return_tensors='tf', padding=True, truncation=True, max_length=128)['input_ids']
        query_embedding = self.phobert_model(input_ids)[0]
        query_embedding = tf.reduce_mean(query_embedding, axis=1).numpy()
        D, I = self.index.search(query_embedding, top_k)
        return self.knowledge_base.iloc[I[0]]

# Khởi tạo Retriever với đường dẫn tới file CSV
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
phobert_model = TFAutoModel.from_pretrained("vinai/phobert-base")
retriever = Retriever('knowledge_base.csv', tokenizer, phobert_model)

# Hàm predict_problem sử dụng Retriever
def predict_problem(problem):
    retrieved_problems = retriever.retrieve(problem)
    augmented_input = " ".join([problem] + retrieved_problems['problem'].tolist())
    input_ids, attention_mask = encode_texts([augmented_input], tokenizer, max_len)
    prediction = model.predict({'input_ids': input_ids, 'attention_mask': attention_mask})
    probabilities = prediction[0]
    adjusted_probabilities = adjust_probabilities(problem, probabilities, uniform_keywords, accelerated_keywords)
    predicted_label_index = np.argmax(adjusted_probabilities)
    predicted_label = list(label_dict.keys())[list(label_dict.values()).index(predicted_label_index)]
    return predicted_label

user_states = {}

@app.route('/chat', methods=['POST'])
def chat():
    global user_states
    data = request.get_json()

    user_id = data.get('userId')
    if not user_id:
        return jsonify({'error': 'Thiếu userId'}), 400

    if user_id not in user_states:
        user_states[user_id] = {
            "mode": "normal",
            "predicted_label": None,
            "difficulty_level": None
        }

    state = user_states[user_id]

    if 'message' in data:
        message = data['message'].lower()
    # elif 'image' in data:
    #     image_data = base64.b64decode(data['image'])
    #     image_content = io.BytesIO(image_data).read()
    #     credentials_path = 'rapid-stage-425307-j4-58d15bd4cd2e.json'  # Thay bằng đường dẫn thực tế của bạn
    #     message = detect_text(image_content, credentials_path)
    #     if not message:
    #         return jsonify({'error': 'Không thể nhận dạng văn bản từ ảnh'}), 400
    else:
        return jsonify({'error': 'Thiếu thông điệp hoặc ảnh'}), 400

    if state["mode"] == "normal":
        for keyword, response in topics.items():
            if keyword in message:
                if keyword == "bài tập":
                    state["mode"] = "predict_physics"
                    return jsonify({"response": "Hãy gửi bài tập cho tôi."})
                else:
                    return jsonify({"response": response})
        return jsonify({"response": "Chào bạn, tôi chưa được học kiến thức này, nếu cần tạo bài tập hãy tìm tôi nhé"})
    
    elif state["mode"] == "predict_physics":
        cleaned_text = clean_text(message)
        predicted_label = predict_problem(cleaned_text)
        state["mode"] = "ask_difficulty_level"
        state["predicted_label"] = predicted_label  
        return jsonify({"response": f"Kết quả dự đoán: {predicted_label}. Bạn muốn tạo bài ở mức độ nào, tôi có thể tạo ở các mức sau: thông hiểu, vận dụng, vận dụng cao."})
    

    elif state["mode"] == "ask_difficulty_level":
        difficulty_levels = ["thông hiểu", "vận dụng", "vận dụng cao"]
        stop_word = ["stop"]
        if message in stop_word:
            state["mode"] = "predict_physics"
            return jsonify({"response": f"xin lỗi vì sự sai sót này, bạn hãy thử tạo lại một bài tập khác nhé 😇🥺😵"})
                    
        if message in difficulty_levels:
            state["difficulty_level"] = message
            state["mode"] = "ask_number_of_problems"
            return jsonify({"response": f"Bạn muốn tạo bao nhiêu bài dạng {state['predicted_label']} ở mức độ {state['difficulty_level']}?"})
        
        else:
            return jsonify({"response": "Vui lòng chọn một trong các mức độ: thông hiểu, vận dụng, vận dụng cao."})

    elif state["mode"] == "ask_number_of_problems":
        try:
            num_problems = int(message)
            # ------------------------------------------------------------------------------------------------------------
            # ---------------------------------------Vận dụng------------------------------------------------------------
            if state["predicted_label"] == "chuyển động thẳng biến đổi đều" and state["difficulty_level"] == "vận dụng" and isinstance(num_problems, int):
                problems = []
                for _ in range(num_problems):
                    problem, solution = generate_problem_and_solution()
                    problems.append({"problem": problem, "solution": solution})
                
                state["mode"] = "normal"
                return jsonify({
                    "response": f"Đã tạo {num_problems} bài tập ở mức độ vận dụng.",
                    "problems": problems
                })
            
            if state["predicted_label"] == "chuyển động thẳng đều" and state["difficulty_level"] == "vận dụng" and isinstance(num_problems, int):
                problems = []
                for _ in range(num_problems):
                    problem, solution = generate_problem_and_solution_2()
                    problems.append({"problem": problem, "solution": solution})
                
                state["mode"] = "normal"
                return jsonify({
                    "response": f"Đã tạo {num_problems} bài tập ở mức độ vận dụng.",
                    "problems": problems
                })

            if state["predicted_label"] == "chuyển động ném xiên" and state["difficulty_level"] == "vận dụng" and isinstance(num_problems, int):
                problems = []
                for _ in range(num_problems):
                    problem, solution = generate_problem_and_solution_7()
                    problems.append({"problem": problem, "solution": solution})
                
                state["mode"] = "normal"
                return jsonify({
                    "response": f"Đã tạo {num_problems} bài tập ở mức độ vận dụng.",
                    "problems": problems
                })

            if state["predicted_label"] == "rơi tự do" and state["difficulty_level"] == "vận dụng" and isinstance(num_problems, int):
                problems = []
                for _ in range(num_problems):
                    problem, solution = generate_problem_and_solution_3()
                    problems.append({"problem": problem, "solution": solution})
                
                state["mode"] = "normal"
                return jsonify({
                    "response": f"Đã tạo {num_problems} bài tập ở mức độ vận dụng.",
                    "problems": problems
                })
            

            # ------------------------------------------------------------------------------------------------------------
            # ---------------------------------------vận dụng cao------------------------------------------------------------
       

            if state["predicted_label"] == "chuyển động thẳng biến đổi đều" and state["difficulty_level"] == "vận dụng cao" and isinstance(num_problems, int):
                problems = []
                for _ in range(num_problems):
                    problem, solution = generate_problem_and_solution_6()
                    problems.append({"problem": problem, "solution": solution})
                
                state["mode"] = "normal"
                return jsonify({
                    "response": f"Đã tạo {num_problems} bài tập ở mức độ vận dụng cao.",
                    "problems": problems
                })
            
            if state["predicted_label"] == "chuyển động thẳng đều" and state["difficulty_level"] == "vận dụng cao" and isinstance(num_problems, int):
                problems = []
                for _ in range(num_problems):
                    problem, solution = generate_problem_and_solution_5()
                    problems.append({"problem": problem, "solution": solution})
                
                state["mode"] = "normal"
                return jsonify({
                    "response": f"Đã tạo {num_problems} bài tập ở mức độ vận dụng cao.",
                    "problems": problems
                })

            if state["predicted_label"] == "chuyển động ném xiên" and state["difficulty_level"] == "vận dụng cao" and isinstance(num_problems, int):
                problems = []
                for _ in range(num_problems):
                    problem, solution = generate_problem_and_solution_7()
                    problems.append({"problem": problem, "solution": solution})
                
                state["mode"] = "normal"
                return jsonify({
                    "response": f"Đã tạo {num_problems} bài tập ở mức độ vận dụng cao.",
                    "problems": problems
                })

            if state["predicted_label"] == "rơi tự do" and state["difficulty_level"] == "vận dụng cao" and isinstance(num_problems, int):
                problems = []
                for _ in range(num_problems):
                    problem, solution = generate_problem_and_solution_3()
                    problems.append({"problem": problem, "solution": solution})
                
                state["mode"] = "normal"
                return jsonify({
                    "response": f"Đã tạo {num_problems} bài tập ở mức độ vận dụng cao.",
                    "problems": problems
                })
            
            else:
                state["mode"] = "normal"
                return jsonify({"response": "Dạng bài tập không phù hợp hoặc mức độ hoặc số lượng bài tập không hợp lệ."})

        except ValueError:
            return jsonify({"response": "Vui lòng nhập một số hợp lệ."})
    
    # Đặt lại chế độ về normal sau khi xử lý từng chủ đề cụ thể
    state["mode"] = "normal"
    return jsonify({"response": "Xin chào! Bạn cần giúp gì?"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)