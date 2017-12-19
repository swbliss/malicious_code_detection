
import tensorflow as tf
import numpy as np
from model import CharCNN
import data_helper

# Load data
print("Loading data...")
n_test_samples = 100
x, y = data_helper.load_data()

x_test, y_test = x[-n_test_samples:], y[-n_test_samples:]

with tf.Graph().as_default():
    with tf.Session() as sess:
        cnn = CharCNN()
        saver = tf.train.Saver()
        saver.restore(sess, "/home/swjung/cs548/runs/1480429434/checkpoints/model-40")

        x_batch_test, y_batch_test = data_helper.get_shaped_batch_input(x_test, y_test, 0, n_test_samples)
        feed_dict = {
            cnn.input_x: x_batch_test,
            cnn.input_y: y_batch_test,
            cnn.dropout_keep_prob: 1.0
        }

        prediction = sess.run(cnn.predictions, feed_dict)
        scores = sess.run(cnn.scores, feed_dict)
        print('#################ANSWER#################')
        print(y_batch_test)
        print('#################PREDICTION#################')
        print(prediction)
        print('#################SCORES#################')
        print(scores)
        print('============================')
        result = (tf.equal(prediction, tf.argmax(y_batch_test, 1)))

        
        all_vars = tf.trainable_variables()
        for v in all_vars:
            print(sess.run(v.value()))
        

        print(np.count_nonzero(result.eval()))
