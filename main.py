
from flask import Flask, jsonify, request, redirect, render_template, flash,jsonify
import numpy as np
from werkzeug.utils import secure_filename
import os
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
import tensorflow as tf
from keras.applications.vgg16 import preprocess_input



UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__) 
app.config["JSON_AS_ASCII"] = False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# TFliteモデルのロード
interpreter = tf.lite.Interpreter(model_path = "converted_model.tflite")
interpreter.allocate_tensors()


class result_dict:
    results = dict()
  
#ルーティング
@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/result', methods=['POST'])
def result():
        file = request.files['upload_image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            #表示したいクラス名
            label=['ドクツルタケ',
                   'ホンシメジ',
                   'ヒラタケ',
                   'ムキタケ',
                   'ニセクロハツ',
                   'スギヒラタケ',
                   'シイタケ',
                   'ツキヨタケ']
            # 画像のロード & 正規化
            img = img_to_array(load_img(img_path, target_size=(224, 224)))
            input_img = preprocess_input(img)

            # モデルの入出力情報の取得
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            # 入力画像のshapeを整形
            input_data = np.expand_dims(input_img, axis = 0)

            # 予測
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()

            # 予測結果の出力
            output_data = interpreter.get_tensor(output_details[0]['index'])
            predict = int(np.argmax(output_data))
            name = label[predict]
            print(name,predict)
        return jsonify(name,predict)
    
 
@app.route('/results',methods=['GET', 'POST'])
def ajaxtest():
    if request.method == "POST":
        file = request.files['upload_image']

    
        return render_template("./index.html")
 
    return render_template("./index.html")
 
 #起動
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
