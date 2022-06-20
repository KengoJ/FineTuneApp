from flask import Flask, jsonify, request, redirect, render_template, flash,jsonify
import numpy as np
from werkzeug.utils import secure_filename
import os
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
import tensorflow as tf
from keras.applications.vgg16 import preprocess_input
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import datetime


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__) 
app.config["JSON_AS_ASCII"] = False
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Results(db.Model):
    __tablename__ = 'Resluts'
    id = db.Column(db.Integer,primary_key=True)
    img_name = db.Column(db.Text)
    predict_res = db.Column(db.Text)
    upload_date = db .Column(db.DateTime)

    def __init__(self, img_name=None, predict_res=None, upload_date=None):
        self.img_name = img_name
        self.predict_res = predict_res
        self.upload_date = upload_date

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# TFliteモデルのロード
interpreter = tf.lite.Interpreter(model_path = "converted_model.tflite")
interpreter.allocate_tensors()


#ルーティング
@app.route('/')
def index():
    label=['ドクツルタケ',
                   'ホンシメジ',
                   'ヒラタケ',
                   'ムキタケ',
                   'ニセクロハツ',
                   'スギヒラタケ',
                   'シイタケ',
                   'ツキヨタケ']
    return render_template('./index.html',label=label)

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
          
            #結果をデータベースに登録
            sendresult = Results(filename,name,datetime.datetime.now())
            db.session.add(sendresult)
            db.session.commit()
        return jsonify(name,predict)
    
@app.route('/history',methods=['GET','POST'])
def history():
    data = Results.query.order_by(desc(Results.upload_date)).limit(10).all()
    return render_template('./history.html',data=data)

#起動
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
