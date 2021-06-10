from flask import Flask, request, redirect, url_for, render_template


from werkzeug import datastructures #werkzeug라이브러리로 import해야하나?
from werkzeug.utils import redirect
import sys
print(sys.version)
# 모델에 필요한 모듈들을 import

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Input, LSTM, Embedding, Dense, Masking, Concatenate
from tensorflow.keras.models import Model
from tensorflow.python.keras.callbacks import ModelCheckpoint
from tensorflow.python.ops.variables import global_variables_initializer
import re
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from tensorflow.keras.preprocessing.text import Tokenizer
from keras_preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import urllib.request
np.random.seed(seed=0)

import model.seq2seq_attention_only_review as prem


#지금은 /result 루트를 통해 원문을 받았고 result페이지에 원문, 요약문 넣어주는 부분에 넣었거든./result에 모델코드 다 집어 넣어서 다 여기서 처리하도록 
# base.html(POST-원문)-> /result함수에서 processing(원문)-modeling-predict(요약문)-> ->result.html에 함께 띄우기
#


app = Flask(__name__)#static_url_path='/static'이 필요하나?

#사전에 학습된 모델(model폴더에 있음)을 아래에 불러옴 


src_index_to_word = prem.src_tokenizer.index_word # 원문 단어 집합에서 정수 -> 단어를 얻음
tar_word_to_index = prem.tar_tokenizer.word_index # 요약 단어 집합에서 단어 -> 정수를 얻음
tar_index_to_word = prem.tar_tokenizer.index_word # 요약 단어 집합에서 정수 -> 단어를 얻음

encoder_model = Model(prem.encoder_inputs, [prem.encoder_outputs, prem.h_state, prem.c_state])

encoder_h_state = Input(shape=(50,))
encoder_c_state = Input(shape=(50,))

pd_decoder_outputs, pd_h_state, pd_c_state = prem.decoder_lstm(prem.decoder_mask, initial_state=[encoder_h_state, encoder_c_state])

# 어텐션 구현부
# 2089는 시점 (단어, 패딩) 의 수, 50은 히든 스테이트의 차원
pd_encoder_outputs = Input(shape=(prem.text_max_len, 50))
pd_attn_out, pd_attn_states = prem.attn_layer([pd_encoder_outputs, pd_decoder_outputs])
pd_decoder_concat = Concatenate()([pd_decoder_outputs, pd_attn_out])

pd_decoder_softmax_outputs = prem.decoder_dense(pd_decoder_concat)

decoder_model = Model([prem.decoder_inputs, pd_encoder_outputs, encoder_h_state, encoder_c_state], [pd_decoder_softmax_outputs, pd_h_state, pd_c_state])

#########################################저장된 모델 불러오기
saver = tf.train.Saver()
model = global_variables_initializer()

sess = tf.Session() #세션 객체 생성, 사용자 요청이 들어올 때마다 모델을 학습시킬수 있게 함
sess.run(model)

#저정된 모델이 세션에 적용될 수 있게 모델 저장할 곳(save_path) 지정	

save_path = './model/review_summaization_new.h5'
#방금 돌린 모델(세션)을 페스에 restore	
saver.restore(sess, save_path)



@app.route('/')
def base():
	
	return render_template('base.html')#render로 base 템플릿을 띄워줌




@app.route('/result', methods=['POST'])#form으로 받은 원문이 전달되는 주소.(여기서 모델을 실행시켜야..) 
def result():
	if request.method == 'POST':
		
		

		input_stc =  request.form["original"] #사용자가 입력한 값을 전달받아 input_stc에 저장
		
		#입력 데이터 전처리파트를 아래에 작성
		token_stc = input_stc.split()
		encode_stc = tokenizer_from_json.texts_to_sequences([token_stc])
		pad_stc = pad_sequences(encode_stc, maxlen=prem.text_max_len, padding="POST")


################################


		#인코딩 부분
		
		en_out, en_hidden, en_cell = encoder_model.predict(pad_stc)

		predicted_seq = np.zeros((1,1))
		predicted_seq[0, 0] = prem.su_to_index['sostoken']


		#디코딩 부분
		decoded_stc = []

		while True:
			output_words, h, c = decoder_model.predict([predicted_seq, en_out, en_hidden, en_cell])#디코딩용 모델 불러와서 예측

			predicted_word = prem.index_to_su[np.argmax(output_words[0,0])]

			if predicted_word == 'eostoken':
				break

			decoded_stc.append(predicted_word)

			predicted_seq = np.zeros((1,1))
			predicted_seq[0, 0] = np.argmax(output_words[0, 0])

			en_hidden = h
			en_cell = c

		print('\n')
		summary = ' '.join(decoded_stc)#생성된 요약문을 담는 변수

		model.save('model/model/review_summaization_new.h5')# 경로를어떻게해야하지

		



	return render_template('result.html', origins = input_stc, summ = summary)#render할 때 원문, 요약문도 함께 전달하기



if __name__ == '__main__':
	app.run(debug=True)#포트 설정은 다음에