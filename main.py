
from flask import Flask, jsonify, request, redirect, render_template, flash,jsonify
import numpy as np
from werkzeug.utils import secure_filename
import os
from keras.utils import img_to_array, load_img
#from keras.models import load_model
import numpy as np
import tensorflow as tf
from keras.applications.inception_v3 import preprocess_input
#from keras.preprocessing.image import array_to_img, img_to_array, load_img


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__) 
app.config["JSON_AS_ASCII"] = False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#学習済みモデルの読込
#model=load_model('./model.h5', compile = False)

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
            """
            img = img_to_array(load_img(img_path, target_size=(224,224)))
            #0-1に変換
            img_nad = img_to_array(img)/255
            #4次元配列に
            img_nad = img_nad[None, ...]
            #表示したいクラス名
            label=['ドクツルタケ',
                   'ホンシメジ',
                   'ヒラタケ',
                   'ムキタケ',
                   'ニセクロハツ',
                   'スギヒラタケ',
                   'シイタケ',
                   'ツキヨタケ']
            
            #判別
            pred = model.predict(img_nad, batch_size=1, verbose=0)
            #判別結果で最も高い数値を抜き出し
            score = np.max(pred)
            #判別結果の配列から最も高いところを抜きだし、そのクラス名をpred_labelへ
            pred_label = label[np.argmax(pred[0])]
            #表示
            print('name:',pred_label)
            print('score:',score)
            print(filename)
            answer = pred_label
            result_dict.results.setdefault(filename,answer)
            print(result_dict.results)
            """

            
            # 画像のロード & 正規化
            img = img_to_array(load_img(img_path, target_size=(224, 224)))
            input_img = preprocess_input(img)

            # TFliteモデルのロード
            interpreter = tf.lite.Interpreter(model_path = "converted_model.tflite")
            interpreter.allocate_tensors()

            # モデルの入出力情報の取得
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            # 入力画像のshapeを整形
            input_data = np.expand_dims(input_img, axis = 0)

            # 予測
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])


            # 予測結果の出力
            print(output_data.argmax(axis = 1))
        return jsonify(output_data)
    
 
@app.route('/results',methods=['GET', 'POST'])
def ajaxtest():
    if request.method == "POST":
        file = request.files['upload_image']

    
        return render_template("./index.html")
 
    return render_template("./index.html")
 
 #起動
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
