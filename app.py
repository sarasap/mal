from flask import Flask, request, jsonify, render_template
from tensorflow.keras.preprocessing.text import Tokenizer
import pandas as pd
from tensorflow.keras.preprocessing import sequence
import tensorflow as tf
import Extraction

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    f=request.files['file']
    f.save(f.filename)
    data=Extraction.extration_code(f.filename)
    max_words = 1000
    max_len = 34063
    tok = Tokenizer(num_words=max_words)
    df = pd.DataFrame(data,index=[0])
    sequences = tok.texts_to_sequences(df["clean_seq"])
    sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)
    model = tf.keras.models.load_model('mod.h5')
    y_pred = model.predict(sequences_matrix)
    y_pred_flat = y_pred.flatten()
    if y_pred_flat[0]>=0.5:
        result='malware'
    else:
        result='benign'
    return render_template('prediction.html',pred=result)
