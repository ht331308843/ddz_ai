import tensorflow.compat.v1 as tf
import numpy as np
import random 
from threading import Timer
import time
import logging
from flask import Flask, request
import json
from numpy.core.defchararray import array

logging.basicConfig(filename="../flaskLog/log.txt",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
__path__ = '../model_save/model'

App = Flask(__name__)  

def play(observation):
	re = [0]
	with tf.Session() as sess:
		saver=tf.train.import_meta_graph(__path__+".meta")
		saver.restore(sess, __path__)
		graph = tf.get_default_graph()
		_inputX = graph.get_tensor_by_name('dqn_target_q/X:0')
		is_train = graph.get_tensor_by_name('dqn_target_q/is_train:0')
		actions = graph.get_tensor_by_name('dqn_target_q/actions:0')
		_outputY = graph.get_tensor_by_name('dqn_target_q/GatherV2:0')
		sess.run(tf.global_variables_initializer())
		re = sess.run([_outputY],feed_dict={_inputX:np.reshape(observation['obs'],(-1,6,5,15)),is_train:False,actions:np.reshape(observation['actions'],(-1))})
	re = array(re)[0]
	i = 1
	tempi = 0
	while i < re.__len__():
		if(re[i] > re[tempi]) :
			tempi = i
		i+=1
	print('in ddz play prediction', observation['actions'],re,tempi)
	return observation['actions'][tempi]

@App.route('/getAiDoAction', methods = ['GET', 'POST'])
def getAiDoAction():
	if request.method == 'POST':
		data = request.get_data()
		# print(data)
		App.logger.info(data)
		json_data = json.loads(data.decode('utf-8'))
		start = time.time()	
		App.logger.info(json_data)
		re_info = play(json_data)
		end = time.time()
		print("time:%.2f s" % (end-start))
		App.logger.info(re_info)
		App.logger.info("[use_time]:%.2f s" % (end-start))
		return json.dumps(re_info)


if __name__ == "__main__":
	
	App.run(debug=True, host='127.0.0.1', port=5000)

	
